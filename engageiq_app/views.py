import json
import base64
import requests
from decimal import Decimal
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from .models import SubscriptionPlan, UserSubscription, BillingRecord
from .utils import (
    extract_document_text, validate_subscription, 
    get_system_prompt, call_openllm, get_custom_social_instructions,
    update_api_usage, get_system_instructions, invoke_llm,
)
from engageiq_app.models import (
    UserSubscription, SubscriptionPlan, APIUsage, 
    SystemPrompt, BillingRecord
)
from accounts.models import User
from .models import EmailMessage
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from datetime import timedelta
from django.utils.timezone import now
from uuid import UUID
from security import safe_requests

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_llm_response(request):
    """
    Handles LLM response generation, supporting optional document processing.
    """
    user = request.user
    data = request.POST

    system_prompt_id = data.get("system_prompt_id")
    company_name = data.get("company_name", "Default Company")
    product_or_service = data.get("product_or_service", "Default Product")
    target_audience = data.get("target_audience", "Default Audience")
    selected_tab = data.get("selected_tab", "").strip().lower()
    custom = data.get("custom", "").strip()  # New custom field

    # Map fields dynamically based on selected_tab
    tab_field_mapping = {
        "features": ["feature1", "feature2", "feature3"],
        "benefits": ["benefit1", "benefit2", "benefit3"],
        "painpoints": ["painpoint1", "painpoint2", "painpoint3"],
        "desires": ["desire1", "desire2", "desire3"]
    }

    # Fetch system prompt
    system_prompt = get_system_prompt(system_prompt_id)
    if isinstance(system_prompt, JsonResponse):
        return system_prompt  # Return error response if fetching system prompt fails
      # Predefined system instructions
    instruction_prompt_text = get_system_instructions()

    # Ensure selected_tab is valid, only for non-Custom Social prompts
    custom_social_prompt_id = UUID("08038bb5-4550-4cfa-b5e5-5ab99a450c3f")
    if system_prompt.id != custom_social_prompt_id:
        if selected_tab not in tab_field_mapping:
            return JsonResponse({"error": f"Invalid selected_tab provided.{selected_tab}"}, status=400)

        field_keys = tab_field_mapping[selected_tab]

        # Extract values from request
        field1 = data.get(field_keys[0], "").strip()
        field2 = data.get(field_keys[1], "").strip()
        field3 = data.get(field_keys[2], "").strip()

        # Ensure at least ONE field is provided
        if not any([field1, field2, field3]):
            return JsonResponse(
                {"error": f"At least one of {field_keys[0]}, {field_keys[1]}, or {field_keys[2]} must be provided."}, 
                status=400
            )

    # Extract document text if a file is uploaded
    document_text = ""
    if "document" in request.FILES:
        document_text = extract_document_text(request.FILES["document"])
        if isinstance(document_text, JsonResponse):
            return document_text  # Return error response if document extraction fails

    # Validate user subscription
    user_subscription = validate_subscription(user)
    if isinstance(user_subscription, JsonResponse):
        return user_subscription

    # Fetch system prompt
    system_prompt = get_system_prompt(system_prompt_id)
    if isinstance(system_prompt, JsonResponse):
        return system_prompt

    # Predefined system instructions
    instruction_prompt_text = get_system_instructions()

    # Logic for "Custom Social"
    if system_prompt.id == UUID("08038bb5-4550-4cfa-b5e5-5ab99a450c3f"):
        # Only include "document_content" and "custom" for Custom Social prompt
        prompt_input_data = {
            "document_content": document_text if document_text else None,
            "custom": custom if custom else None
        }

        instruction_prompt_text = get_custom_social_instructions()
        user_message_text = f"""
        {instruction_prompt_text}
        - **Document Content**: {document_text if document_text else '[No document uploaded]'}
        - **Custom**: {custom if custom else '[No custom content]'}
        """
        
    else:
        # For all other prompts, only include specific fields (company_name, product_or_service, etc.)
        prompt_input_data = {
            "company_name": company_name if company_name else None,  # Exclude if missing
            "product_or_service": product_or_service if product_or_service else None,
            "target_audience": target_audience if target_audience else None,
            "selected_tab": selected_tab if selected_tab else None,
            field_keys[0]: field1 if field1 else None,
            field_keys[1]: field2 if field2 else None,
            field_keys[2]: field3 if field3 else None,
        }

        # Construct the user message text for general prompts
        user_message_text = f"""
        - **Company Name**: {company_name}
        - **Product/Service**: {product_or_service}
        - **Target Audience**: {target_audience}
        - **Selected Tab**: {selected_tab}
        """

        # Add field values dynamically
        for key in [field_keys[0], field_keys[1], field_keys[2]]:
            if key in prompt_input_data:
                user_message_text += f"\n- **{key}**: {prompt_input_data[key]}"

        user_message_text += f"\n\n{document_text if document_text else '[No document uploaded]'}"

    # Call LLM Model
    response_text, metrics = invoke_llm(system_prompt.text_body, instruction_prompt_text, user_message_text)

    # Store response in DB
    EmailMessage.objects.create(
        system_prompt_id=system_prompt_id,
        user=user,
        prompt_input=json.dumps(prompt_input_data),
        llm_response=response_text,
        latency_ms=metrics["latency_ms"],
        cost=metrics["cost"]
    )

    # Update API usage
    update_api_usage(user_subscription, Decimal(metrics["cost"]))

    # Return Response
    return JsonResponse({
        "response": response_text,
        "metrics": metrics,
    }, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_api_usage_details(request):
    """
    Retrieves API usage details for the latest subscription of the authenticated user.
    """
    user = request.user

    # Fetch the latest subscription (active or inactive)
    user_subscription = UserSubscription.objects.filter(user=user).order_by('-current_period_start').first()
    
    if not user_subscription:
        return JsonResponse({"error": "No subscription history found."}, status=404)
    
    # Fetch the latest API usage entry for this subscription
    api_usage = APIUsage.objects.filter(user_subscription=user_subscription).order_by('-id').first()

    return JsonResponse({
        "subscription_plan": user_subscription.subscription_plan.name,
        "status": user_subscription.status,
        "current_period_start": user_subscription.current_period_start,
        "current_period_end": user_subscription.current_period_end,
        "total_api_calls": user_subscription.subscription_plan.Queries,
        "api_calls_done": api_usage.total_api_call_count if api_usage else 0,
        "cost": str(api_usage.cost) if api_usage else "0.0",
    }, status=200)


@api_view(['GET'])
def get_system_prompts(request):
    """
    Retrieves available system prompts.
    """
    prompts = SystemPrompt.objects.filter(is_active=True)
    response_data = [{"id": str(prompt.id), "title": prompt.title, "text_body": prompt.text_body} for prompt in prompts]
    return JsonResponse({"system_prompts": response_data}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_chat_history(request):
    """
    Retrieves chat history for the authenticated user, categorized by today, yesterday,
    last 7 days, and last 30 days.
    """
    user = request.user
    current_time = now()

    # Define date ranges
    today_start = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_start - timedelta(days=1)
    seven_days_start = today_start - timedelta(days=7)
    thirty_days_start = today_start - timedelta(days=30)

    messages = EmailMessage.objects.filter(user=user).order_by('-created_at')

    # Function to format messages
    def format_message(msg):
        try:
            clean_prompt_input = json.loads(msg.prompt_input) if isinstance(msg.prompt_input, str) else msg.prompt_input
        except json.JSONDecodeError:
            clean_prompt_input = {}

        return {
            "id": str(msg.id),
            "llm_response": msg.llm_response,
            "prompt_input": clean_prompt_input,
            "created_at": msg.created_at.isoformat(),
        }

    # Categorize messages
    history = {
        "today": [],
        "yesterday": [],
        "last_7_days": [],
        "last_30_days": [],
    }

    for msg in messages:
        if msg.created_at >= today_start:
            history["today"].append(format_message(msg))
        elif msg.created_at >= yesterday_start:
            history["yesterday"].append(format_message(msg))
        elif msg.created_at >= seven_days_start:
            history["last_7_days"].append(format_message(msg))
        elif msg.created_at >= thirty_days_start:
            history["last_30_days"].append(format_message(msg))

    return JsonResponse({"chat_history": history}, status=200)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_subscription_plans(request):
    """
    Lists available subscription plans ordered by price.
    """
    plans = SubscriptionPlan.objects.all().order_by("price")

    response_data = []
    for plan in plans:
        plan_data = {
            "id": str(plan.id),
            "name": plan.name,
            "price": str(plan.price),
            "billing_cycle": plan.duration,
            "queries": plan.Queries,
            "seats": plan.Seats,
            "target_audience": plan.Target_Audience or "",
            "features": plan.features or "",
            "image_heading": plan.image_heading or "",
            "footer_note": plan.footer_note or "",
            "contact_us": plan.contact_us or "",
            "image": plan.image.name if plan.image else "",
            "logo_image": plan.logo_image.name if plan.logo_image else "",
            "created_at": plan.created_at.isoformat(),
        }

        response_data.append(plan_data)

    return JsonResponse({"plans": response_data}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscription_history(request):
    """
    Retrieves the history of all subscription plans assigned to a user,
    including API usage details. The latest active plan appears first.
    """
    user = request.user
    
    # Fetch subscriptions ordered by latest first
    subscriptions = UserSubscription.objects.filter(user=user).order_by("-created_at")

    if not subscriptions.exists():
        return JsonResponse({"error": "No subscription history found."}, status=404)

    history = []
    
    for sub in subscriptions:
        api_usage = APIUsage.objects.filter(user_subscription=sub).first()

        history.append({
            "Plan_name": sub.subscription_plan.name,
            "Billing_cycle": sub.subscription_plan.duration,
            "Status": sub.status,
            "Current_period_start": sub.current_period_start,
            "Current_period_end": sub.current_period_end,
            "Total_api_calls": sub.subscription_plan.Queries,
            "API_usage": {
                "Api_calls_done": api_usage.total_api_call_count if api_usage else 0,
                "Cost": str(api_usage.cost) if api_usage else "0.00"
            }
        })

    return JsonResponse({"subscription_history": history}, status=200)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def assign_subscription(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)

    # Extract token from Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return JsonResponse({'error': 'Authorization token missing or invalid'}, status=401)

    token = auth_header.split(' ')[1]
    try:
        access_token = AccessToken(token)
        user = User.objects.get(id=access_token['user_id'])
    except (TokenError, InvalidToken):
        # If access token is expired, attempt to refresh it using the provided refresh token
        refresh_token = data.get('refresh')
        if not refresh_token:
            return JsonResponse({'error': 'Refresh token missing in request body'}, status=401)
        try:
            new_access_token = str(RefreshToken(refresh_token).access_token)
            # Update Authorization header with the new token
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
            access_token = AccessToken(new_access_token)  # Revalidate the token
            user = User.objects.get(id=access_token['user_id'])
        except TokenError:
            return JsonResponse({'error': 'Refresh token invalid or expired, please log in again'}, status=401)

    # Check if user exists in the database
    if not User.objects.filter(id=user.id).exists():
        return JsonResponse({'error': 'User not found'}, status=404)
    
    # Extract order ID
    order_id = data.get('orderID')
    if not order_id:
        return JsonResponse({'error': 'Missing order ID'}, status=400)

    # Obtain an access token from PayPal
    auth_response = requests.post(
        'https://api-m.sandbox.paypal.com/v1/oauth2/token',
        headers={
            'Authorization': 'Basic ' + base64.b64encode(f"{settings.PAYPAL_CLIENT_ID}:{settings.PAYPAL_SECRET}".encode()).decode(),
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={'grant_type': 'client_credentials'}
    )
    if auth_response.status_code != 200:
        return JsonResponse({'error': 'Failed to authenticate with PayPal'}, status=500)

    auth_data = auth_response.json()
    access_token = auth_data.get('access_token')
    if not access_token:
        return JsonResponse({'error': 'No access token received'}, status=500)

    # Retrieve order details from PayPal
    order_response = safe_requests.get(
        f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    )
    if order_response.status_code != 200:
        return JsonResponse({'error': 'Failed to retrieve order details'}, status=500)

    order_data = order_response.json()

    # Extract required details
    order_status = order_data.get('status')
    plan_id = data.get("plan_id")
    purchase_unit = order_data.get('purchase_units', [{}])[0]
    transaction_amount = purchase_unit.get('amount', {}).get('value')
    currency = purchase_unit.get('amount', {}).get('currency_code')
    payer_email = order_data.get('payer', {}).get('email_address')
    payer_id = order_data.get('payer', {}).get('payer_id')
    receiver_email = purchase_unit.get('payee', {}).get('email_address')
    receiver_id = purchase_unit.get('payee', {}).get('merchant_id')
    invoice_url = next((link['href'] for link in order_data.get('links', []) if link.get('rel') == 'self'), None)

    # Verify if payment is received in the correct account
    expected_merchant_id = settings.PAYPAL_MERCHANT_ID if hasattr(settings, 'PAYPAL_MERCHANT_ID') else None
    is_valid_receiver = receiver_id == expected_merchant_id
    # Validate the subscription plan
    subscription_plan = SubscriptionPlan.objects.get(id=plan_id)
    if subscription_plan.duration == "annual":
        period_end = now() + timedelta(days=365)  # 1 year
    else:
        period_end = now() + timedelta(days=30) # 1 month
    # Check if the transaction ID already exists to prevent duplicate payments
    if BillingRecord.objects.filter(transaction_id=order_id).exists():
        return JsonResponse({'error': 'Duplicate transaction detected. This payment has already been processed.'}, status=400)
    # Inactivate all existing active subscriptions assigned to the user before assigning the new one
    UserSubscription.objects.filter(user=user, status="active").update(status="inactive")
    # Assign new subscription
    user_subscription = UserSubscription.objects.create(
        user=user,
        subscription_plan=subscription_plan,
        status="active",
        billing_cycle=subscription_plan.duration,
        current_period_start=now(),
        current_period_end=period_end,
    )

    # Store billing record
    BillingRecord.objects.create(
    subscription=user_subscription,
    status="paid",
    transaction_id=order_id, 
    amount=transaction_amount,  
    currency=currency, 
    payer_email=payer_email, 
    invoice_url=invoice_url,
    billing_cycle=subscription_plan.duration, 
    paid_at=timezone.now() 
    )

    # Initialize API usage tracking
    APIUsage.objects.create(
        user_subscription=user_subscription,
        total_api_call_count=0,
        cost=Decimal('0.0')
    )
    # Verify the order
    if order_status == 'COMPLETED' and is_valid_receiver:
        return JsonResponse({
            'status': 'Payment verified',
            'user_id': user.id,
            'order_status': order_status,
            'transaction_amount': transaction_amount,
            'currency': currency,
            'payer_email': payer_email,
            'payer_id': payer_id,
            'receiver_email': receiver_email,
            'receiver_id': receiver_id,
            'is_valid_receiver': is_valid_receiver,
            'assigned_plan': subscription_plan.name if hasattr(subscription_plan, 'name') else 'Unknown Plan'
        })
    else:
        return JsonResponse({'error': 'Payment not completed or incorrect receiver account'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

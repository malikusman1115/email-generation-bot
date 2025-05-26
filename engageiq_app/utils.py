import os
import json
from decimal import Decimal
from PyPDF2 import PdfReader 
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from dotenv import load_dotenv
from langchain.schema import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from engageiq_app.models import APIUsage, SystemPrompt, UserSubscription
import time
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from langchain.callbacks import get_openai_callback
from langchain_groq import ChatGroq

load_dotenv()

MAX_DOCUMENT_LENGTH = 50000 
MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_FILE_TYPES = ["pdf", "txt"]

def extract_document_text(uploaded_file):
    """
    Extracts text from an uploaded PDF or TXT file.
    """
    file_extension = uploaded_file.name.split('.')[-1].lower()
    file_size = uploaded_file.size
    
    if file_size > MAX_FILE_SIZE:
        return JsonResponse({"error": "File size exceeds the 3MB limit."}, status=400)
    
    if file_extension not in ALLOWED_FILE_TYPES:
        return JsonResponse({"error": "Unsupported file format. Only PDF and TXT are allowed."}, status=400)

    document_text = ""
    
    try:
        if file_extension == "pdf":
            pdf_reader = PdfReader(uploaded_file)
            extracted_pages = [page.extract_text() for page in pdf_reader.pages if page.extract_text()]
            document_text = "\n".join(extracted_pages) if extracted_pages else ""
        elif file_extension == "txt":
            document_text = uploaded_file.read().decode("utf-8", errors="ignore").strip()
            if not document_text:
                return JsonResponse({"error": "The uploaded TXT file is empty."}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"File processing error: {str(e)}"}, status=400)
    
    document_text = " ".join(document_text.split())
    return document_text[:MAX_DOCUMENT_LENGTH] + "..." if len(document_text) > MAX_DOCUMENT_LENGTH else document_text

def validate_subscription(user):
    """
    Validates if the user has an active subscription.
    Always fetches the latest active subscription.
    """
    user_subscription = UserSubscription.objects.filter(user=user, status='active').order_by('-created_at').first()
    
    if not user_subscription:
        return JsonResponse({"error": "No active subscription found. Please choose a plan first."}, status=403)

    return user_subscription


def get_system_prompt(system_prompt_id):
    """
    Fetches system prompt by ID.
    """
    if not system_prompt_id:
        return JsonResponse({"error": "System prompt ID is required."}, status=400)
    
    return get_object_or_404(SystemPrompt, id=system_prompt_id, is_active=True)

def get_instructions_prompt():
    """
    Fetches the instructions system prompt.
    """
    try:
        return SystemPrompt.objects.get(title="instructions", is_active=True)
    except SystemPrompt.DoesNotExist:
        return JsonResponse({"error": "Instructions prompt not found."}, status=404)


def call_openllm(system_prompt_text, instruction_prompt_text, user_message_text):
    """
    Calls the OpenAI GPT model and extracts token usage from the response.
    """
    sys_prompt = f"""
    SYSTEM PROMPT:
    {system_prompt_text}

    INSTRUCTIONS:
    {instruction_prompt_text}
    """

    # Initialize OpenAI Chat Model using API key from .env
    model = ChatOpenAI(
        model_name="gpt-4o", 
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0
    )

    messages = [
        SystemMessage(content=sys_prompt),
        HumanMessage(content=user_message_text)
    ]

    start_time = time.time()
    try:
        # Capture Token Usage using OpenAI callback
        with get_openai_callback() as cb:
            output = model.invoke(messages)  # Make API call

            response_text = str(output.content)  
            total_cost = cb.total_cost  

        end_time = time.time()

    except Exception as e:
        print("OpenAI API Error:", str(e))
        raise RuntimeError(f"OpenAI API call failed: {str(e)}") 
    # Calculate latency
    latency_ms = int((end_time - start_time) * 1000)

    # Extracted Token Usage Data
    metrics = {
        "latency_ms": latency_ms,
        "cost": total_cost  
    }

    return response_text, metrics


def invoke_llm(system_prompt_text, instruction_prompt_text, user_message_text):
    """
    Calls the OpenAI GPT model and extracts token usage from the response.
    """
    sys_prompt = f"""
    SYSTEM PROMPT:
    {system_prompt_text}

    INSTRUCTIONS:
    {instruction_prompt_text}
    """

    # Initialize OpenAI Chat Model using API key from .env
    model = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")

    messages = [
        SystemMessage(content=sys_prompt),
        HumanMessage(content=user_message_text)
    ]

    start_time = time.time()
    try:
        # Capture Token Usage using OpenAI callback
        with get_openai_callback() as cb:
            output = model.invoke(messages)  # Make API call
            response_text = str(output.content)  
            total_cost = cb.total_cost  
        end_time = time.time()

    except Exception as e:
        print("OpenAI API Error:", str(e))
        raise RuntimeError(f"OpenAI API call failed: {str(e)}") 
    # Calculate latency
    latency_ms = int((end_time - start_time) * 1000)

    # Extracted Token Usage Data
    metrics = {
        "latency_ms": latency_ms,
        "cost": total_cost  
    }

    return response_text, metrics


def update_api_usage(user_subscription, cost):
    """
    Updates API usage for the most recent subscription.
    A new APIUsage row is created for every new plan assignment.
    """
    # Ensure that we fetch the latest subscription API usage entry
    api_usage = APIUsage.objects.filter(user_subscription=user_subscription).order_by('-id').first()

    if not api_usage:
        return JsonResponse({"error": "No API usage record found for the current subscription."}, status=404)

    api_usage.cost += cost
    api_usage.total_api_call_count += 1
    api_usage.save()

    # Fetch the related subscription plan
    subscription_plan = user_subscription.subscription_plan

    # Check if limits are exceeded (but do NOT block the current API call)
    if api_usage.total_api_call_count >= subscription_plan.Queries:
        user_subscription.status = 'inactive'
        user_subscription.save()

    return True

def get_user_subscription_history(user):
    """
    Retrieves all past and current subscriptions of a user.
    """
    subscriptions = UserSubscription.objects.filter(user=user).select_related("subscription_plan").order_by("-created_at")
    
    history = []
    for sub in subscriptions:
        history.append({
            "plan_name": sub.subscription_plan.name,
            "status": sub.status,
            "current_period_start": sub.current_period_start,
            "current_period_end": sub.current_period_end,
            "cancellation_date": sub.cancellation_date
        })
    
    return history


def get_system_instructions():
    """
    Returns the predefined system instructions instead of fetching from the database.
    """
    return """
    - You must evaluate the user's input and classify if they are talking about something general, 
      or they have provided the data that is to be used to generate an email for them.
    - If the user's input is generic, you must only reply with "Ready." to highlight that you are ready 
      to receive the data and generate the email.
    - If the user has provided you the data in the input, YOU MUST NOT say ready again. Instead, 
      you should now use that data to generate the email in your response and follow the system prompt.
    - Make sure to exactly follow the guideline provided in the SYSTEM PROMPT section 
      for the generation of every email.
    """

def get_custom_social_instructions():
    """
    Returns the predefined instructions for the 'Custom Social' prompt.
    """
    return """
    **Instruction:** Always generate a full response based on the available input.
    - If a document is uploaded, use it along with the provided details.
    - If no document is uploaded, rely entirely on the user’s input fields.
    - NEVER return "Ready."
    """

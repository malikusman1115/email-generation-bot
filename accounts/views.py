from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from engageiq_app.models import UserSubscription, SubscriptionPlan
from django.contrib.auth import authenticate, logout, get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from datetime import timedelta
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    OTPSerializer,
    PasswordResetRequestSerializer,
    PasswordResetVerifySerializer,
    PasswordResetSerializer
)
from .models import OTP, User

from engageiq_app.models import (
    UserSubscription,
    SubscriptionPlan,
    APIUsage,
    SystemPrompt
)
import string
import logging
import json
import os
from datetime import datetime
from decimal import Decimal
from rest_framework.permissions import AllowAny 
import logging
import secrets

logger = logging.getLogger(__name__)

User = get_user_model() 


def generate_otp():
    return ''.join(secrets.SystemRandom().choices(string.digits, k=6))


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def resend_otp(request):
    email = request.data.get('email')
    purpose = request.data.get('purpose')  

    if not email or not purpose:
        return Response({"error": "Email and purpose are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # If purpose is 'SIGNUP', check if the email is already registered
        if purpose == 'SIGNUP' and User.objects.filter(email=email).exists():
            return Response({"error": "Email is already registered. Please log in instead."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Get existing OTP
        existing_otp = OTP.objects.filter(email=email, purpose=purpose, is_verified=False).first()

        # Check if existing OTP is still valid
        if existing_otp and hasattr(existing_otp, 'is_valid') and existing_otp.is_valid():
            return Response({"message": "Existing OTP is still valid. Please check your email."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Preserve registration_data from the previous OTP (For SIGNUP purpose)
        registration_data = existing_otp.registration_data if existing_otp else None

        # Delete expired OTP before creating a new one
        if existing_otp:
            existing_otp.delete()

        # Generate and store new OTP
        otp = generate_otp()
        new_otp = OTP.objects.create(
            email=email,
            otp=otp,
            purpose=purpose,
            registration_data=registration_data  # Preserve registration data from old OTP
        )

        # Send the new OTP via email
        if send_otp_email(email, otp, purpose):
            return Response({"message": "OTP resent successfully.", "email": email}, status=status.HTTP_200_OK)
        else:
            logger.error(f"Failed to send OTP to {email}")  
            new_otp.delete() 
            return Response({"error": "Failed to resend OTP email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        logger.error(f"Error in resend_otp API: {str(e)}")  
        return Response({"error": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def send_otp_email(email, otp, purpose):
    subject = {
        'SIGNUP': 'Verify Your Email for Registration',
        'LOGIN': 'Login Verification Code',
        'RESET': 'Password Reset Code'
    }.get(purpose, 'Verification Code')

    message = f"""
Hello!

Your verification code is: {otp}

This code will expire in 1 minute.

If you didn't request this code, please ignore this email.

Best regards,
Your Team
    """

    try:
        logger.info(f"Attempting to send email to {email} with OTP: {otp}")
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        logger.info(f"OTP sent successfully to {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send OTP email to {email}: {str(e)}")
        return False


class SignupAPIView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            try:
                email = serializer.validated_data['email']
                otp = generate_otp()

                # Remove existing unverified OTPs
                OTP.objects.filter(email=email, purpose='SIGNUP', is_verified=False).delete()

                # Save OTP object
                otp_obj = OTP.objects.create(
                    email=email,
                    otp=otp,
                    purpose='SIGNUP',
                    registration_data=serializer.validated_data
                )

                if send_otp_email(email, otp, 'SIGNUP'):
                    return Response({'message': 'OTP sent successfully', 'email': email})
                else:
                    otp_obj.delete()
                    return Response({'error': 'Failed to send OTP email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                logger.error(f"Registration error: {str(e)}")
                return Response({'error': 'Registration failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]  
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Authenticate user
            user = authenticate(request, email=email, password=password)

            if user:
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)

                # Combine all details in response
                response_data = {
                    "message": "Login successful",
                    "user_id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    # "subscription": subscription_data,
                    # "api_usage": api_usage_data,
                    "access": str(refresh.access_token),  # Include JWT token
                    "refresh": str(refresh)
                }

                return Response(response_data, status=status.HTTP_200_OK)

            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        try:
            email = serializer.validated_data['email']
            contact_number = serializer.validated_data.get('contact_number')  # Ensure this is captured
            otp = generate_otp()

            if User.objects.filter(email=email).exists():
                return Response({"error": "Email is already registered. Please log in instead."}, 
                                status=status.HTTP_400_BAD_REQUEST)

            # Delete expired OTPs before generating a new one
            OTP.objects.filter(email=email, purpose='SIGNUP', is_verified=False).delete()

            # Ensure `registration_data` contains `contact_number`
            registration_data = serializer.validated_data.copy()
            registration_data['contact_number'] = contact_number  

            otp_obj = OTP.objects.create(
                email=email,
                otp=otp,
                purpose='SIGNUP',
                registration_data=registration_data  # Store contact_number properly
            )

            if send_otp_email(email, otp, 'SIGNUP'):
                return Response({'message': 'OTP sent successfully', 'email': email})
            else:
                otp_obj.delete()
                return Response({'error': 'Failed to send OTP email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return Response({'error': 'Registration failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from engageiq_app.models import UserSubscription, SubscriptionPlan

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_registration_otp(request):
    serializer = OTPSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        try:
            otp_obj = OTP.objects.filter(email=email, otp=otp, purpose='SIGNUP', is_verified=False).first()

            if not otp_obj:
                return Response({'error': 'Invalid OTP or email.'}, status=status.HTTP_400_BAD_REQUEST)

            # Ensure `registration_data` is valid and contains `contact_number`
            registration_data = otp_obj.registration_data
            if not isinstance(registration_data, dict) or "contact_number" not in registration_data:
                return Response({'error': 'Invalid registration data. Contact number missing.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            # Create the user
            user = User.objects.create_user(
                email=email,
                password=registration_data['password1'],  
                first_name=registration_data.get('first_name', ''),  
                last_name=registration_data.get('last_name', ''),  
                contact_number=registration_data['contact_number']
            )

            # Automatically assign the Sandbox plan
            period_end = now() + timedelta(days=30) # 1 month
            plan_id = "d57a6e13-af84-427e-a65e-593b5f2e141f"
            sandbox_plan = SubscriptionPlan.objects.get(id=plan_id)
            sandbox_plan.duration == "monthly"
            user_subscription = UserSubscription.objects.create(
                user=user,
                subscription_plan=sandbox_plan,
                status="active",
                billing_cycle=sandbox_plan.duration,
                current_period_start=now(),
                current_period_end=period_end,
            )
            APIUsage.objects.create(
            user_subscription=user_subscription,
            total_api_call_count=0,
            cost=Decimal('0.0')
    )

            # Mark OTP as verified
            otp_obj.is_verified = True
            otp_obj.user = user
            otp_obj.save()

            # Create JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'Registration successful and Sandbox plan assigned',
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)

        except SubscriptionPlan.DoesNotExist:
            return Response({'error': 'Sandbox plan not found.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset(request):
    serializer = PasswordResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            otp = generate_otp()

            #Check if a valid OTP already exists before generating a new one
            existing_otp = OTP.objects.filter(email=email, purpose='RESET', is_verified=False).first()
            if existing_otp and hasattr(existing_otp, 'is_valid') and existing_otp.is_valid():
                return Response({'message': 'Existing OTP is still valid. Please check your email.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            #Remove expired OTPs before generating a new one
            OTP.objects.filter(email=email, purpose='RESET', is_verified=False).delete()

            #Save new OTP object
            otp_obj = OTP.objects.create(
                email=email,
                otp=otp,
                purpose='RESET'
            )

            #Attempt to send the OTP email
            if send_otp_email(email, otp, 'RESET'):
                return Response({'message': 'OTP sent successfully', 'email': email}, status=status.HTTP_200_OK)
            else:
                # Cleanup if sending the email fails
                otp_obj.delete()
                return Response({'error': 'Failed to send OTP email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except User.DoesNotExist:
            return Response({'error': 'Email not registered.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_reset_otp(request):
    serializer = PasswordResetVerifySerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        try:
            otp_obj = OTP.objects.filter(email=email, otp=otp, purpose='RESET', is_verified=False).first()

            if not otp_obj:
                return Response({'error': 'Invalid OTP or email'}, status=status.HTTP_400_BAD_REQUEST)

            if not otp_obj.is_valid():
                return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)

            # Mark OTP as verified
            otp_obj.is_verified = True
            otp_obj.verified_at = timezone.now()
            otp_obj.save()

            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']

        try:
            otp_obj = OTP.objects.filter(email=email, purpose='RESET', is_verified=True).first()

            if not otp_obj:
                return Response({'error': 'OTP not verified or request invalid'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch user safely
            user = User.objects.filter(email=email).first()
            if not user:
                return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

            # Reset password
            user.set_password(new_password)
            user.save()

            # Delete OTP after successful password reset
            otp_obj.delete()

            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def check_email(request):
    email = request.data.get('email')
    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"message": "Email is already registered"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Email is not registered"}, status=status.HTTP_200_OK)

from django.urls import path
from .views import (
    SignupAPIView, LoginAPIView, verify_registration_otp, register_user,check_email,
    request_password_reset, verify_reset_otp, reset_password, LogoutAPIView, resend_otp
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login_api"),
    path("register/", register_user, name="register_user"),
    path("verify-registration-otp/", verify_registration_otp, name="verify_registration_otp"),
    path("request-password-reset/", request_password_reset, name="request_password_reset"),
    path("verify-reset-otp/", verify_reset_otp, name="verify_reset_otp"),
    path("reset-password/", reset_password, name="reset_password"),
    path("resend-otp/", resend_otp, name="resend_otp"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("check_email/", check_email, name="check_email"), 
]

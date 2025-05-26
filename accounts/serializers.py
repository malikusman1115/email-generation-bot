from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()  # Ensure correct User model

class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    contact_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    class Meta:
        model = User  
        fields = ['email', 'password1', 'password2', 'contact_number', 'first_name', 'last_name']  
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'contact_number': {'required':False}
        }

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password1'], 
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()  
    password = serializers.CharField(write_only=True, max_length=128)

# OTP Serializer
class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6, min_length=6)

# Password Reset Serializers
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6, min_length=6)

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta

#  Custom User Manager to properly handle user creation
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)  
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

#  Custom User Model
class User(AbstractUser):
    username = None  
    email = models.EmailField(unique=True) 
    first_name = models.CharField(max_length=30, blank=True, null=True)  
    last_name = models.CharField(max_length=30, blank=True, null=True) 
    contact_number = models.CharField(max_length=11, blank=True, null=True)


    #  Fix conflicting related_name attributes
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",  
        blank=True
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"] 

    objects = CustomUserManager()  

    def __str__(self):
        return self.email


# OTP Model (No change needed)
class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    purpose = models.CharField(
        max_length=20,
        choices=[
            ('SIGNUP', 'Signup Verification'),
            ('LOGIN', 'Login Verification'),
            ('RESET', 'Password Reset')
        ]
    )
    registration_data = models.JSONField(null=True, blank=True, db_column='registration_data')

    def is_valid(self):
        """Checks if the OTP is still valid based on the creation time."""
        return (timezone.now() - self.created_at) < timedelta(minutes=1)

    def __str__(self):
        """Returns a string representation of the OTP instance."""
        return f"OTP({self.otp}, Purpose: {self.purpose}, Verified: {self.is_verified})"

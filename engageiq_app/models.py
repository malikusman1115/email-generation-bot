import uuid
from django.db import models
from accounts.models import User
from django.conf import settings
import uuid

# Subscription Plans Table
def subscription_image_upload_path(instance, filename):
    return f'about_us/{filename}'

def enterprise_logo_upload_path(instance, filename):
    return f'about_us/enterprise_logos/{filename}'

class SubscriptionPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00)
    Queries = models.BigIntegerField(null=False, default=0)
    Seats = models.PositiveIntegerField(null=False, default=1)
    Target_Audience = models.CharField(max_length=100, null=True, blank=True)
    features = models.TextField(null=True, blank=True)
    duration = models.CharField(
        max_length=10,
        choices=[("monthly", "Monthly"), ("annual", "Annual")],
        default="monthly"
    )
    image = models.ImageField(upload_to=subscription_image_upload_path, null=True, blank=True)
    image_heading = models.CharField(max_length=200, null=True, blank=True)
    logo_image = models.ImageField(upload_to=enterprise_logo_upload_path, null=True, blank=True) 
    footer_note = models.CharField(max_length=255, null=True, blank=True)  
    contact_us = models.URLField(max_length=300, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.duration})"

    @property
    def show_image(self):
        return not self.name.lower().startswith("sandbox")


    
# Updated UserSubscription Model
class UserSubscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    subscription_plan = models.ForeignKey('SubscriptionPlan', on_delete=models.CASCADE)
    
    # Status of the subscription
    status = models.CharField(max_length=50, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ], default='inactive')  
    
    # New Field: Billing cycle (monthly vs. annual)
    billing_cycle = models.CharField(max_length=10, choices=[
        ('monthly', 'Monthly'),
        ('annual', 'Annual')
    ], blank=True, null=True) 
    
    # Subscription period tracking
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    
    # Tracking cancellations
    cancellation_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.subscription_plan.name if self.subscription_plan else 'No Plan'} ({self.billing_cycle})"


# EmailMessage Model
class EmailMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    system_prompt_id = models.UUIDField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    prompt_input = models.JSONField(null=True, blank=True)
    llm_response = models.TextField(null=True, blank=True)
    latency_ms = models.IntegerField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=6, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"EmailMessage by {self.user.email}"  


# Billing Records Table
class BillingRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE)
    
    # Status of the billing
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    
    # Payment details
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)  
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
    currency = models.CharField(max_length=10, null=True, blank=True) 
    payer_email = models.EmailField(null=True, blank=True)  
    invoice_url = models.CharField(max_length=255, null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # New Field: Billing cycle tracking
    billing_cycle = models.CharField(max_length=10, choices=[
        ('monthly', 'Monthly'),
        ('annual', 'Annual')
    ],blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"BillingRecord for {self.subscription} - {self.status} - {self.billing_cycle}"


# API Usage Table
class APIUsage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=6, null=False, default=0.000000)
    total_api_call_count = models.BigIntegerField(null=False, default=0)  
    updated_at = models.DateTimeField(auto_now=True)



# System Prompts Table
class SystemPrompt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    text_body = models.TextField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
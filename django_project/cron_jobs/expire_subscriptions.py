import os
import django
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
import sys

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

# Add the project root directory to `sys.path`
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Move two directories up (to Backend_Lauri)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Initialize Django
django.setup()

from engageiq_app.models import UserSubscription

def send_email_notification(user_email):
    """
    Sends an email to the user notifying them that their subscription has expired.
    """
    subject = "Subscription Expired - Action Required"
    message = """
    Your subscription has expired. To continue using our services, please renew your subscription.
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])

def expire_subscriptions():
    """
    Checks for expired subscriptions and marks them as inactive.
    """
    now = timezone.now()
    expired_subscriptions = UserSubscription.objects.filter(status='active', current_period_end__lt=now)

    for subscription in expired_subscriptions:
        subscription.status = 'expire'  
        subscription.save()
        
        print(f"Subscription for {subscription.user.email} has been set to inactive.")

        # Send email notification
        send_email_notification(subscription.user.email)

if __name__ == "__main__":
    expire_subscriptions()

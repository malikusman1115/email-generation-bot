from django.core.management.base import BaseCommand
from engageiq_app.models import SubscriptionPlan

class Command(BaseCommand):
    help = "Populate or update subscription plans in the database"

    def handle(self, *args, **kwargs):
        latest_plans = {
            "Sandbox (Monthly)",
            "Basic (Monthly)",
            "Basic (Annual)",
            "Pro (Monthly)",
            "Pro (Annual)",
            "Business+ (Monthly)",
            "Business+ (Annual)",
            "Enterprise (Annual)"
        }

        SubscriptionPlan.objects.exclude(name__in=latest_plans).delete()

        plans = [
            {
                "name": "Sandbox (Monthly)",
                "duration": "monthly",
                "price": 0.00,
                "Queries": 3,
                "Seats": 1,
                "Target_Audience": "Startups/Testers",
                "features": (
                    "✔ Free to Get Started\n"
                    "✔ No credit card required."
                ),
            },
            {
                "name": "Basic (Monthly)",
                "duration": "monthly",
                "price": 29.00,
                "Queries": 90,
                "Seats": 1,
                "Target_Audience": "Solo Creators/Freelancers",
                "features": (
                    "✔ Beyond Basic Customized Messaging\n"
                    "✔ Subject Line Optimization\n"
                    "✔ Email Support\n"
                    "✔ OTP\n"
                    "✔ Security Features?"
                ),
                "image_heading": "Build like:",
            },
            {
                "name": "Basic (Annual)",
                "duration": "annual",
                "price": 290.00,
                "Queries": 900,
                "Seats": 1,
                "Target_Audience": "Solo Creators/Freelancers",
                "features": (
                    "✔ Beyond Basic Customized Messaging\n"
                    "✔ Subject Line Optimization\n"
                    "✔ Email Support\n"
                    "✔ OTP\n"
                    "✔ Security Features?"
                ),
                "image_heading": "Build like:",
            },
            {
                "name": "Pro (Monthly)",
                "duration": "monthly",
                "price": 99.00,
                "Queries": 250,
                "Seats": 2,
                "Target_Audience": "Small Teams",
                "features": (
                    "✔ Advanced Customized Messaging\n"
                    "✔ Profile & Psychology Insights Application\n"
                    "✔ Subject Line Optimization\n"
                    "✔ On Demand Value Matrix Sales Training\n"
                    "✔ Priority Email Support\n"
                    "✔ OTP\n"
                    "✔ Security Features?"
                ),
                "image_heading": "Automate like:",
            },
            {
                "name": "Pro (Annual)",
                "duration": "annual",
                "price": 990.00,
                "Queries": 2500,
                "Seats": 2,
                "Target_Audience": "Small Teams",
                "features": (
                    "✔ Advanced Customized Messaging\n"
                    "✔ Profile & Psychology Insights Application\n"
                    "✔ Subject Line Optimization\n"
                    "✔ On Demand Value Matrix Sales Training\n"
                    "✔ Priority Email Support\n"
                    "✔ OTP\n"
                    "✔ Security Features?"
                ),
                "image_heading": "Automate like:",
            },
            {
                "name": "Business+ (Monthly)",
                "duration": "monthly",
                "price": 299.00,
                "Queries": 600,
                "Seats": 5,
                "Target_Audience": "Scaling Companies",
                "features": (
                    "✔ Advanced Customized Messaging\n"
                    "✔ Deeper Profile & Psychology Insights Application\n"
                    "✔ Subject Line Optimization\n"
                    "✔ Custom Social\n"
                    "✔ X Knowledge Base Sources\n"
                    "✔ OTP\n"
                    "✔ Live Value Matrix Sales Training\n"
                    "✔ Priority + Phone Support\n"
                    "✔ Security Features?"
                ),
                "image_heading": "Scale like:",
            },
            {
                "name": "Business+ (Annual)",
                "duration": "annual",
                "price": 2990.00,
                "Queries": 6000,
                "Seats": 5,
                "Target_Audience": "Scaling Companies",
                "features": (
                    "✔ Advanced Customized Messaging\n"
                    "✔ Deeper Profile & Psychology Insights Application\n"
                    "✔ Subject Line Optimization\n"
                    "✔ Custom Social\n"
                    "✔ X Knowledge Base Sources\n"
                    "✔ OTP\n"
                    "✔ Live Value Matrix Sales Training\n"
                    "✔ Priority + Phone Support\n"
                    "✔ Security Features?"
                ),
                "image_heading": "Scale like:",
            },
            {
                "name": "Enterprise (Annual)",
                "duration": "annual",
                "Target_Audience": "Large Brands",
                "features": (
                    "✔ Enterprise Package\n"
                    "✔ For Established Brands Desiring to Commercialize\n"
                    "✔ or Create a Competitive Edge\n\n"
                    "✔ Custom Pricing\n"
                ),
                "image_heading": "Go Commercial or Establish Your Edge like:",
                "footer_note": "We’re excited to serve you!",
                "contact_us": "https://yourdomain.com/contact-us"
            },
        ]


        for plan in plans:
            defaults = {
                "duration": plan["duration"],
                "Target_Audience": plan["Target_Audience"],
                "features": plan["features"],
                "image_heading": plan.get("image_heading", ""),
                "footer_note": plan.get("footer_note", ""),
                "contact_us": plan.get("contact_us", ""),
            }

            # Add these only if the keys exist (i.e., skip them for Enterprise)
            if "price" in plan:
                defaults["price"] = plan["price"]
            if "Queries" in plan:
                defaults["Queries"] = plan["Queries"]
            if "Seats" in plan:
                defaults["Seats"] = plan["Seats"]

            obj, created = SubscriptionPlan.objects.update_or_create(
                name=plan["name"],
                defaults=defaults
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Added: {plan['name']}"))
            else:
                self.stdout.write(self.style.WARNING(f"🔁 Updated: {plan['name']}"))


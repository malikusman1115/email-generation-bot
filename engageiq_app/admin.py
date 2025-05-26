from django.contrib import admin
from django.utils.html import format_html
from .models import SubscriptionPlan, UserSubscription, EmailMessage, BillingRecord, APIUsage, SystemPrompt

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        "name", "duration", "Target_Audience",
        "price_display", "Queries_display", "Seats_display",
        "preview_image", "preview_logo_image", "contact_us", "footer_note"
    )
    readonly_fields = ["preview_image", "preview_logo_image", "footer_note", "contact_us"]

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 80px;" />', obj.image.url)
        return "—"

    def preview_logo_image(self, obj):
        if obj.logo_image:
            return format_html('<img src="{}" style="height: 80px;" />', obj.logo_image.url)
        return "—"

    def price_display(self, obj):
        return "" if "Enterprise" in obj.name else obj.price

    def Queries_display(self, obj):
        return "" if "Enterprise" in obj.name else obj.Queries

    def Seats_display(self, obj):
        return "" if "Enterprise" in obj.name else obj.Seats

    def get_fields(self, request, obj=None):
        fields = ["name", "duration", "Target_Audience", "features"]

        if obj:
            if "Pro" in obj.name:
                fields += [
                    "image_heading",
                    "image", "preview_image",
                    "logo_image", "preview_logo_image"
                ]
            elif "Enterprise" in obj.name:
                fields += [
                    "image_heading",
                    "image", "preview_image",
                    "footer_note", "contact_us"
                ]
            else:
                fields += [
                    "price", "Queries", "Seats",
                    "image", "preview_image"
                ]

        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ["preview_image", "preview_logo_image"]
        if obj and "Enterprise" in obj.name:
            fields += ["footer_note", "contact_us"]
        return fields

admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(UserSubscription)
admin.site.register(EmailMessage)
admin.site.register(BillingRecord)
admin.site.register(APIUsage)
admin.site.register(SystemPrompt)

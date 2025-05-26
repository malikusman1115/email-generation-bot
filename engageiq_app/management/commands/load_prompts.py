"""
This script deletes all existing system prompts and loads new ones.
It ensures the database has only the latest active prompts.
"""

from django.core.management.base import BaseCommand
from engageiq_app.models import SystemPrompt
from engageiq_app.data.get_prompts import prompts  

class Command(BaseCommand):
    help = "Delete old system prompts and load new ones"

    def handle(self, *args, **kwargs):
        # Step 1: Delete all existing system prompts
        deleted_count, _ = SystemPrompt.objects.all().delete()
        self.stdout.write(self.style.ERROR(f"Deleted {deleted_count} existing system prompts."))

        # Step 2: Insert new prompts
        for title, text_body in prompts.items():
            prompt = SystemPrompt.objects.create(
                title=title,
                text_body=text_body,
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS(f"Added new prompt: {title}"))

        self.stdout.write(self.style.SUCCESS("🎉 System prompts have been successfully updated!"))

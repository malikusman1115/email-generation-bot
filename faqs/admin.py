from django.contrib import admin
from .models import FAQ, UserQuestion

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'created_at']
    search_fields = ['question', 'answer']
    ordering = ['-created_at']

@admin.register(UserQuestion)
class UserQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'created_at', 'is_answered', 'answer']
    search_fields = ['question', 'answer']
    ordering = ['-created_at']
    fields = ['question', 'answer', 'is_answered'] 
    readonly_fields = ['created_at', 'updated_at']

    def save_model(self, request, obj, form, change):
        """Automatically mark as answered when an admin adds a reply and update the FAQ table"""
        if obj.answer and not obj.is_answered:
            # Mark the question as answered
            obj.is_answered = True

            # Check if the question already exists in the FAQ table
            faq_entry, created = FAQ.objects.update_or_create(
                question=obj.question,  # If a question exists, update it
                defaults={'answer': obj.answer}  # Update the answer if the question is found
            )

            # If it didn't exist, a new FAQ entry will be created
            if created:
                faq_entry.save()

        # Save the UserQuestion model after updates
        super().save_model(request, obj, form, change)

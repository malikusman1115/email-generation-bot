from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class UserQuestion(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_answered = models.BooleanField(default=False)  
    def __str__(self):
        return self.question
    
@receiver(post_save, sender=UserQuestion)
def create_faq_from_answered_question(sender, instance, created, **kwargs):
    """
    Whenever a UserQuestion is saved with is_answered=True,
    create an FAQ entry if one doesn't already exist.
    """
    # Only proceed if the question is answered
    if instance.is_answered:
        # Either create a new FAQ or retrieve the existing one 
        # (e.g., if question text is unique, you can rely on that uniqueness).
        FAQ.objects.get_or_create(
            question=instance.question,
            defaults={'answer': instance.answer}
        )
from rest_framework import serializers
from .models import FAQ, UserQuestion

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'created_at']


class UserQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuestion
        fields = ['id', 'question', 'answer', 'created_at', 'is_answered']

        # Make `question` optional for PUT requests, only `answer` is required
        extra_kwargs = {
            'question': {'required': False}  # Make `question` field optional for PUT requests
        }

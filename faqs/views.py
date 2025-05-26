from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import FAQ, UserQuestion
from .serializers import FAQSerializer, UserQuestionSerializer

# List and create FAQs
class FAQListCreateView(generics.ListCreateAPIView):
    queryset = FAQ.objects.all().order_by('-created_at')  # List FAQs ordered by creation time
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]  # Allow any user to access this view

# List and create user questions (only unanswered questions)
class UserQuestionListCreateView(generics.ListCreateAPIView):
    queryset = UserQuestion.objects.filter(is_answered=False).order_by('-created_at')  # Only unanswered questions
    serializer_class = UserQuestionSerializer
    permission_classes = [AllowAny]  # Allow any user to access this view

    def perform_create(self, serializer):
        # Save the user question
        serializer.save()


from django.urls import path
from .views import FAQListCreateView, UserQuestionListCreateView

urlpatterns = [
    # API to list and create FAQs
    path('faqs/', FAQListCreateView.as_view(), name='faq-list-create'),

    # API to list and create user questions (unanswered questions only)
    path('user-questions/', UserQuestionListCreateView.as_view(), name='user-question-list-create'),
]

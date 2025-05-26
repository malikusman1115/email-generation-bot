from django.urls import path
from .views import generate_llm_response, get_api_usage_details,get_system_prompts, get_chat_history,assign_subscription, list_subscription_plans,subscription_history,assign_subscription
urlpatterns = [
    path("generate_llm_response/", generate_llm_response, name="generate_llm_response"),
    path("get_api_usage_details/", get_api_usage_details, name="get_api_usage_details"),
    path("get_system_prompts/", get_system_prompts, name="get_system_prompts"),
    path("get_chat_history/", get_chat_history, name="get_chat_history"),
    path('assign_subscription/', assign_subscription, name='assign_subscription'),
    path('list_subscription_plans/', list_subscription_plans, name='list_subscription_plans'),
    path('subscription_history/', subscription_history, name='subscription_history')
]

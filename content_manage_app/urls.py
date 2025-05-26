from django.urls import path
from .views import HeroSectionContentView, StatsSectionContentView,WorkingSectionContentView, SolutionSectionContentView, LayoutContentView, VideoSectionContentView, PaypalSectionContentView, DashboardContentView, AboutUsContentView, ContactUsCreateView

urlpatterns = [
    path('hero-section/', HeroSectionContentView.as_view(), name='hero-section'),
    path('stats-section/', StatsSectionContentView.as_view(), name='stats-section'),
    path('working-section/', WorkingSectionContentView.as_view(), name='working-section'),
    path('solution-section/', SolutionSectionContentView.as_view(), name='solution-section'),
    path('layout/', LayoutContentView.as_view(), name='layout'),
    path('video-section/', VideoSectionContentView.as_view(), name='video-section'),
    path('paypal-section/', PaypalSectionContentView.as_view(), name='paypal-section'),
    path('dashboard-content/', DashboardContentView.as_view(), name='dashboard-content'),
    path('about-us/', AboutUsContentView.as_view(), name='about-us-content'),
    path('contact-us/', ContactUsCreateView.as_view(), name='contact-us'),
]

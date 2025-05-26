from rest_framework import generics
from rest_framework.permissions import AllowAny 
from .models import (
    HeroSectionContent, StatsSectionContent, WorkingSectionContent,
    SolutionSectionContent, LayoutContent, VideoSectionContent,
    PaypalSectionContent, DashboardContent, AboutUsContent, ContactUs
)
from .serializers import (
    HeroSectionContentSerializer, StatsSectionContentSerializer, WorkingSectionContentSerializer,
    SolutionSectionContentSerializer, LayoutContentSerializer, VideoSectionContentSerializer,
    PaypalSectionContentSerializer, DashboardContentSerializer, AboutUsContentSerializer, ContactUsSerializer
)


class HeroSectionContentView(generics.RetrieveUpdateAPIView):
    queryset = HeroSectionContent.objects.all()
    serializer_class = HeroSectionContentSerializer
    permission_classes = [AllowAny]  

    def get_object(self):
        obj, _ = HeroSectionContent.objects.get_or_create(id=1)
        return obj


class StatsSectionContentView(generics.RetrieveUpdateAPIView):
    queryset = StatsSectionContent.objects.all()
    serializer_class = StatsSectionContentSerializer
    permission_classes = [AllowAny]  
    def get_object(self):
        obj, _ = StatsSectionContent.objects.get_or_create(id=1)
        return obj

class WorkingSectionContentView(generics.RetrieveUpdateAPIView):
    queryset = WorkingSectionContent.objects.all()
    serializer_class = WorkingSectionContentSerializer
    permission_classes = [AllowAny]  

    def get_object(self):
        obj, _ = WorkingSectionContent.objects.get_or_create(id=1)
        return obj


class SolutionSectionContentView(generics.RetrieveUpdateAPIView):
    queryset = SolutionSectionContent.objects.all()
    serializer_class = SolutionSectionContentSerializer
    permission_classes = [AllowAny]  

    def get_object(self):
        obj, _ = SolutionSectionContent.objects.get_or_create(id=1)
        return obj


class LayoutContentView(generics.RetrieveUpdateAPIView):
    queryset = LayoutContent.objects.all()
    serializer_class = LayoutContentSerializer
    permission_classes = [AllowAny]  

    def get_object(self):
        obj, _ = LayoutContent.objects.get_or_create(id=1)
        return obj

class VideoSectionContentView(generics.RetrieveUpdateAPIView):
    queryset = VideoSectionContent.objects.all()
    serializer_class = VideoSectionContentSerializer
    permission_classes = [AllowAny]  

    def get_object(self):
        obj, _ = VideoSectionContent.objects.get_or_create(id=1)
        return obj


class PaypalSectionContentView(generics.RetrieveUpdateAPIView):
    queryset = PaypalSectionContent.objects.all()
    serializer_class = PaypalSectionContentSerializer
    permission_classes = [AllowAny] 
    def get_object(self):
        obj, _ = PaypalSectionContent.objects.get_or_create(id=1)
        return obj


class DashboardContentView(generics.RetrieveUpdateAPIView):
    queryset = DashboardContent.objects.all()
    serializer_class = DashboardContentSerializer
    permission_classes = [AllowAny]  

    def get_object(self):
        obj, _ = DashboardContent.objects.get_or_create(id=1)
        return obj
    
class AboutUsContentView(generics.RetrieveUpdateAPIView):
    queryset = AboutUsContent.objects.all()
    serializer_class = AboutUsContentSerializer
    permission_classes = [AllowAny] 

    def get_object(self):
        obj, _ = AboutUsContent.objects.get_or_create(id=1)
        return obj
    

class ContactUsCreateView(generics.CreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [AllowAny]

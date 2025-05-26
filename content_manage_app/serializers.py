import os
from rest_framework import serializers
from django.conf import settings
from .models import HeroSectionContent, StatsSectionContent, WorkingSectionContent, SolutionSectionContent, LayoutContent, VideoSectionContent, PaypalSectionContent, DashboardContent, Feature, Solution, BulletPoint, Stat, Tooltip, Module, NavigationItem, SocialLink, CompanyLink, ProductLink, AboutUsContent, ContactUs
from rest_framework import serializers

class HeroSectionContentSerializer(serializers.ModelSerializer):
    blacklogo_url = serializers.SerializerMethodField()
    hero_bottom_right_url = serializers.SerializerMethodField()
    hero_left_url = serializers.SerializerMethodField()
    hero_section_url = serializers.SerializerMethodField()
    hero_top_right_url = serializers.SerializerMethodField()
    tick_url = serializers.SerializerMethodField()

    class Meta:
        model = HeroSectionContent
        fields = [
            'id', 'title', 'subtitle', 'subheading', 'email_placeholder',
            'blacklogo_url', 'hero_bottom_right_url', 'hero_left_url',
            'hero_section_url', 'hero_top_right_url', 'tick_url'
        ]

    def get_blacklogo_url(self, obj):
        return obj.blacklogo.url if obj.blacklogo else None

    def get_hero_bottom_right_url(self, obj):
        return obj.hero_bottom_right.url if obj.hero_bottom_right else None

    def get_hero_left_url(self, obj):
        return obj.hero_left.url if obj.hero_left else None

    def get_hero_section_url(self, obj):
        return obj.hero_section.url if obj.hero_section else None

    def get_hero_top_right_url(self, obj):
        return obj.hero_top_right.url if obj.hero_top_right else None

    def get_tick_url(self, obj):
        return obj.tick.url if obj.tick else None

class BulletPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulletPoint
        fields = ['id', 'text']

class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ['id', 'label', 'value']

class StatsSectionContentSerializer(serializers.ModelSerializer):
    bullet_points = BulletPointSerializer(many=True, read_only=True)
    stats = StatSerializer(many=True, read_only=True)

    main_image_url = serializers.SerializerMethodField()
    left_image_url = serializers.SerializerMethodField()
    right_image_url = serializers.SerializerMethodField()

    class Meta:
        model = StatsSectionContent
        fields = [
            'id', 'title', 'description',
            'bullet_points', 'stats',
            'main_image_url', 'left_image_url', 'right_image_url',
            'sales_messaging_title', 'sales_messaging_description',
        ]

    def get_main_image_url(self, obj):
        if obj.main_image and hasattr(obj.main_image, 'url'):
            return obj.main_image.url
        return None

    def get_left_image_url(self, obj):
        if obj.left_image and hasattr(obj.left_image, 'url'):
            return obj.left_image.url
        return None

    def get_right_image_url(self, obj):
        if obj.right_image and hasattr(obj.right_image, 'url'):
            return obj.right_image.url
        return None


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'title', 'description']

class WorkingSectionContentSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)
    feature_icon_url = serializers.SerializerMethodField()

    class Meta:
        model = WorkingSectionContent
        fields = ['id', 'title', 'description', 'button_text', 'features', 'feature_icon_url']

    def get_feature_icon_url(self, obj):
        if obj.feature_icon and hasattr(obj.feature_icon, 'url'):
            return obj.feature_icon.url 
        return None


class SolutionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Solution
        fields = ['id', 'title', 'description', 'image_url']

    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url  
        return None

class SolutionSectionContentSerializer(serializers.ModelSerializer):
    solutions = SolutionSerializer(many=True, read_only=True)

    class Meta:
        model = SolutionSectionContent
        fields = ['id', 'title', 'description', 'solutions']


class NavigationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavigationItem
        fields = ['id', 'label', 'url']

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['id', 'platform', 'url']

class CompanyLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyLink
        fields = ['id', 'label', 'url']

class ProductLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLink
        fields = ['id', 'label', 'url']

class LayoutContentSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    navigation_items = NavigationItemSerializer(many=True, read_only=True)
    social_links = SocialLinkSerializer(many=True, read_only=True)
    company_links = CompanyLinkSerializer(many=True, read_only=True)
    product_links = ProductLinkSerializer(many=True, read_only=True)

    class Meta:
        model = LayoutContent
        fields = [
            'id', 'logo_url',
            'social_heading', 
            'navigation_items', 'social_links',
            'company_links', 'product_links'
        ]

    def get_logo_url(self, obj):
        return obj.logo.url if obj.logo else None
class ModuleSerializer(serializers.ModelSerializer):
    video_url = serializers.SerializerMethodField()
    video_thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ['id', 'title', 'video_url', 'video_thumbnail_url']

    def get_video_url(self, obj):
        return obj.video.url if obj.video else None

    def get_video_thumbnail_url(self, obj):
        return obj.video_thumbnail.url if obj.video_thumbnail else None

class VideoSectionContentSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = VideoSectionContent
        fields = ['id', 'title', 'description', 'modules']


class PaypalSectionContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaypalSectionContent
        fields = ['id', 'title', 'heading', 'description', 'success_message']

class TooltipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tooltip
        fields = ['id', 'title', 'description']

class DashboardContentSerializer(serializers.ModelSerializer):
    tooltips = TooltipSerializer(many=True, read_only=True)

    border_url = serializers.SerializerMethodField()
    edit_url = serializers.SerializerMethodField()
    header_img_url = serializers.SerializerMethodField()
    home_url = serializers.SerializerMethodField()
    training_url = serializers.SerializerMethodField()
    usage_url = serializers.SerializerMethodField()

    class Meta:
        model = DashboardContent
        fields = [
            'id', 'title', 'heading', 'tooltips',
            'border_url','edit_url', 'header_img_url',
            'home_url', 'training_url', 'usage_url'
        ]

    def get_border_url(self, obj): return obj.border.url if obj.border else None
    def get_edit_url(self, obj): return obj.edit.url if obj.edit else None
    def get_header_img_url(self, obj): return obj.header_img.url if obj.header_img else None
    def get_home_url(self, obj): return obj.home.url if obj.home else None
    def get_training_url(self, obj): return obj.training.url if obj.training else None
    def get_usage_url(self, obj): return obj.usage.url if obj.usage else None

class AboutUsContentSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = AboutUsContent
        fields = ['id', 'heading', 'description', 'image_url']

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None    


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at']

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value

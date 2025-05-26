from django.contrib import admin
from django.utils.html import format_html
from .models import (
    HeroSectionContent,
    StatsSectionContent,
    WorkingSectionContent,
    SolutionSectionContent,
    VideoSectionContent,
    PaypalSectionContent,
    LayoutContent,
    DashboardContent,
    Feature, Solution, BulletPoint, Stat, Tooltip, Module, NavigationItem, SocialLink, CompanyLink, ProductLink, AboutUsContent, ContactUs
)


class HeroSectionContentAdmin(admin.ModelAdmin):
    list_display = ['title']
    readonly_fields = [
        'preview_blacklogo', 'preview_hero_bottom_right', 'preview_hero_left',
        'preview_hero_section', 'preview_hero_top_right', 'preview_tick'
    ]

    def preview_blacklogo(self, obj):
        if obj.blacklogo:
            return format_html('<img src="{}" width="100" />', obj.blacklogo.url)
        return "No Image"

    def preview_hero_bottom_right(self, obj):
        if obj.hero_bottom_right:
            return format_html('<img src="{}" width="100" />', obj.hero_bottom_right.url)
        return "No Image"

    def preview_hero_left(self, obj):
        if obj.hero_left:
            return format_html('<img src="{}" width="100" />', obj.hero_left.url)
        return "No Image"

    def preview_hero_section(self, obj):
        if obj.hero_section:
            return format_html('<img src="{}" width="100" />', obj.hero_section.url)
        return "No Image"

    def preview_hero_top_right(self, obj):
        if obj.hero_top_right:
            return format_html('<img src="{}" width="100" />', obj.hero_top_right.url)
        return "No Image"

    def preview_tick(self, obj):
        if obj.tick:
            return format_html('<img src="{}" width="100" />', obj.tick.url)
        return "No Image"

admin.site.register(HeroSectionContent, HeroSectionContentAdmin)

class BulletPointInline(admin.TabularInline):
    model = BulletPoint
    extra = 0

class StatInline(admin.TabularInline):
    model = Stat
    extra = 0

class StatsSectionContentAdmin(admin.ModelAdmin):
    inlines = [BulletPointInline, StatInline]
    list_display = ('title', 'main_image_preview', 'left_image_preview', 'right_image_preview')
    readonly_fields = ('main_image_preview', 'left_image_preview', 'right_image_preview')

    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" width="100" style="object-fit:contain;" />', obj.main_image.url)
        return "No Image"

    def left_image_preview(self, obj):
        if obj.left_image:
            return format_html('<img src="{}" width="100" style="object-fit:contain;" />', obj.left_image.url)
        return "No Image"

    def right_image_preview(self, obj):
        if obj.right_image:
            return format_html('<img src="{}" width="100" style="object-fit:contain;" />', obj.right_image.url)
        return "No Image"

admin.site.register(StatsSectionContent, StatsSectionContentAdmin)

class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 0

class WorkingSectionContentAdmin(admin.ModelAdmin):
    inlines = [FeatureInline]
    list_display = ('title', 'button_text', 'feature_icon_preview')
    readonly_fields = ('feature_icon_preview',)

    def feature_icon_preview(self, obj):
        if obj.feature_icon:
            return format_html('<img src="{}" width="100" height="100" style="object-fit:contain;" />', obj.feature_icon.url)
        return "No Image"
    feature_icon_preview.short_description = 'Feature Icon Preview'

admin.site.register(WorkingSectionContent, WorkingSectionContentAdmin)


class SolutionInline(admin.StackedInline): 
    model = Solution
    extra = 0
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit:contain;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image Preview"

class SolutionSectionContentAdmin(admin.ModelAdmin):
    inlines = [SolutionInline]
    list_display = ['title']

admin.site.register(SolutionSectionContent, SolutionSectionContentAdmin)

class ModuleInline(admin.StackedInline): 
    model = Module
    extra = 0
    readonly_fields = ['preview_video', 'preview_thumbnail']

    def preview_video(self, obj):
        if obj.video:
            return format_html(
                '<video width="200" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>',
                obj.video.url
            )
        return "No Video"

    def preview_thumbnail(self, obj):
        if obj.video_thumbnail:
            return format_html('<img src="{}" width="100" style="object-fit:contain;" />', obj.video_thumbnail.url)
        return "No Thumbnail"

class ModuleInline(admin.StackedInline): 
    model = Module
    extra = 0
    readonly_fields = ['preview_video', 'preview_thumbnail']

    def preview_video(self, obj):
        if obj.video:
            return format_html(
                '<video width="200" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>',
                obj.video.url
            )
        return "No Video"

    def preview_thumbnail(self, obj):
        if obj.video_thumbnail:
            return format_html('<img src="{}" width="100" style="object-fit:contain;" />', obj.video_thumbnail.url)
        return "No Thumbnail"

class VideoSectionContentAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]

admin.site.register(VideoSectionContent, VideoSectionContentAdmin)

@admin.register(PaypalSectionContent)
class PaypalSectionContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'heading', 'description', 'success_message')

class NavigationItemInline(admin.TabularInline):
    model = NavigationItem
    extra = 0

class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 0

class CompanyLinkInline(admin.TabularInline):
    model = CompanyLink
    extra = 0

class ProductLinkInline(admin.TabularInline):
    model = ProductLink
    extra = 0

class LayoutContentAdmin(admin.ModelAdmin):
    inlines = [NavigationItemInline, SocialLinkInline, CompanyLinkInline, ProductLinkInline]
    readonly_fields = ['preview_logo']
    list_display = ['preview_logo', 'social_heading']

    def preview_logo(self, obj):
        if obj.logo and hasattr(obj.logo, 'url'):
            return format_html('<img src="{}" width="100" />', obj.logo.url)
        return "No Logo"

admin.site.register(LayoutContent, LayoutContentAdmin)

class TooltipInline(admin.TabularInline):
    model = Tooltip
    extra = 0

class DashboardContentAdmin(admin.ModelAdmin):
    inlines = [TooltipInline]
    list_display = ('title', 'heading')
    readonly_fields = [
        'preview_border','preview_edit',
        'preview_header_img', 'preview_home',
        'preview_training', 'preview_usage'
    ]

    def _preview(self, image):
        if image:
            return format_html('<img src="{}" width="100" style="object-fit:contain;" />', image.url)
        return "No Image"

    def preview_border(self, obj): return self._preview(obj.border)
    def preview_edit(self, obj): return self._preview(obj.edit)
    def preview_header_img(self, obj): return self._preview(obj.header_img)
    def preview_home(self, obj): return self._preview(obj.home)
    def preview_training(self, obj): return self._preview(obj.training)
    def preview_usage(self, obj): return self._preview(obj.usage)

admin.site.register(DashboardContent, DashboardContentAdmin)

class AboutUsContentAdmin(admin.ModelAdmin):
    readonly_fields = ['preview_image']
    list_display = ['heading', 'preview_image']

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="120" style="object-fit:contain;" />', obj.image.url)
        return "No Image Uploaded"

admin.site.register(AboutUsContent, AboutUsContentAdmin)

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    search_fields = ['name', 'email', 'subject']

admin.site.register(ContactUs, ContactUsAdmin)
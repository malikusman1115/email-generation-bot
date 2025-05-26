from django.contrib import admin
from django import forms
from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget
from .models import Post

class PostAdminForm(forms.ModelForm):
    sections = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        model = Post
        fields = ['user', 'title', 'slug', 'description', 'sections', 'image']  # <-- Added here

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    readonly_fields = ['preview_image']
    list_display = ('id', 'user', 'title', 'created_at', 'preview_image')
    search_fields = ('title', 'user__email')
    prepopulated_fields = {'slug': ('title',)}

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="120" style="object-fit:contain;" />', obj.image.url)
        return "No Image Uploaded"


from rest_framework import serializers
from .models import Post

class PostListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'image_url'] 

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    sections = serializers.JSONField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'title', 'slug', 'description', 'sections',
            'image_url', 'created_at'
        ]

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

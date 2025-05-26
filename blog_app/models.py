from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import JSONField 
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
import os

from accounts.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # <-- New field here
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    sections = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.title

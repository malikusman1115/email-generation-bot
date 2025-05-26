import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("accounts.urls")),  # Account-related API URLs
    path("api/", include("engageiq_app.urls")),  # Engageiq app API URLs
    path("api/", include('blog_app.urls')),  # Blog app API URLs
    path("api/", include("content_manage_app.urls")),  # Content management API URLs
    path("api/", include("faqs.urls")),  # FAQs API URLs
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

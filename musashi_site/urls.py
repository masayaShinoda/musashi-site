from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from base.views import tinymce_image_upload


urlpatterns = [
    path('siteadmin/', admin.site.urls),
    path('', include('base.urls')),
    path('products/', include('products.urls')),

    path('tinymce/', include('tinymce.urls')),
    path('admin/tinymce-upload/', tinymce_image_upload, name="tinymce_upload"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]

admin.site.site_header = "Musashi Lubricants Admin"
admin.site.site_title = "Musashi Lubricants Admin Portal"
admin.site.index_title = "Welcome to Musashi Lubricants Admin Portal"

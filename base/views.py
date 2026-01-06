import os
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
from base.utils import compress_image
from .models import LinkPageDescription, Link


@require_http_methods(['GET'])
def homepage(request):
    context = {"test": "hi"}
    return render(request, 'pages/homepage.html', context)


@require_http_methods(['GET'])
def links_page(request):
    description = LinkPageDescription.objects.first()
    links = Link.objects.all()

    context = {
        'description': description,
        'links': links,
    }

    return render(request, 'pages/links_page.html', context)


@csrf_exempt
def tinymce_image_upload(request):
    if request.method == "POST":
        image = request.FILES.get("file")
        if not image:
            return JsonResponse({"error": "No file"}, status=400)

        # 🔑 Compress the image before saving
        ext = os.path.splitext(image.name)[1].lower()
        fmt = "PNG" if ext in [".png"] else "JPEG"
        compressed = compress_image(
            image, max_size=1400, quality=90, format=fmt)

        # Build a safe filename
        filename = f"tinymce/{os.path.basename(image.name)}"

        # Save the compressed image
        path = default_storage.save(filename, compressed)

        # Use /media/ URL (relative, works fine with TinyMCE in admin)
        image_url = f"{settings.MEDIA_URL}{path}"

        return JsonResponse({"location": image_url})

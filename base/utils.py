"""Project-wide utility functions."""
import os
from datetime import timedelta
from io import BytesIO

from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image, ImageFile

# Allows Pillow to load truncated image files
ImageFile.LOAD_TRUNCATED_IMAGES = True


def compress_image(image, max_size=1500, quality=90, format='JPEG'):
    """
    Compresses and resizes the given image while maintaining aspect ratio.
    Args:
        image (ImageField): The image to process.
        max_size (int): The maximum width or height for resizing.
        quality (int): The quality for JPEG compression (1-100).
        format (str): The output format ('JPEG' or 'PNG').
    Returns:
        ContentFile: The processed image file.
    """
    img = Image.open(image)
    output = BytesIO()

    # Convert RGBA to RGB for JPEG format to avoid errors
    if format == 'JPEG' and img.mode == 'RGBA':
        img = img.convert('RGB')

    # Resize image if it exceeds the max_size
    if img.width > max_size or img.height > max_size:
        if img.width > img.height:
            new_width = max_size
            aspect_ratio = img.height / img.width
            new_height = int(new_width * aspect_ratio)
        else:
            new_height = max_size
            aspect_ratio = img.width / img.height
            new_width = int(new_height * aspect_ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Save the processed image to the BytesIO object
    img.save(output, format=format,
             quality=quality if format == 'JPEG' else None)
    output.seek(0)

    #  Use os.path.basename to get only the filename
    # This ensures that 'upload_to' is applied only once by Django's storage.
    return ContentFile(output.read(), name=os.path.basename(image.name))


def time_since(date):
    """
    Returns a human-readable string of the time elapsed since a given date.
    e.g., "today", "3 days ago", "2 weeks ago"
    """
    now = timezone.now()
    delta = now - date

    if delta < timedelta(days=1):
        return "today"
    elif delta < timedelta(weeks=1):
        days = delta.days
        return f"{days} day ago" if days == 1 else f"{days} days ago"
    elif delta < timedelta(weeks=4):
        weeks = delta.days // 7
        return f"{weeks} week ago" if weeks == 1 else f"{weeks} weeks ago"
    elif delta < timedelta(days=365):
        months = delta.days // 30
        return f"{months} month ago" if months == 1 else f"{months} months ago"
    else:
        years = delta.days // 365
        return f"{years} year ago" if years == 1 else f"{years} years ago"

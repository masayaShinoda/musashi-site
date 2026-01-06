from django.db import models
from django.core.exceptions import ValidationError
from base.utils import compress_image
from tinymce import models as tinymce_models


class LinkPageDescription(models.Model):
    heading = models.CharField(max_length=255, default="")
    description = tinymce_models.HTMLField(default='')

    def save(self, *args, **kwargs):
        # Check if any instance of the model already exists
        if LinkPageDescription.objects.exists() and not self.pk:
            raise ValidationError(
                "Only one instance of this model is allowed.")

        # Call the original save method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.heading}"


class Link(models.Model):
    label = models.CharField(max_length=50, default="")
    url = models.CharField(max_length=255, default="")
    icon = models.ImageField(upload_to='links_page/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.icon:
            self.icon = compress_image(
                self.icon, max_size=512, format='PNG')
        # Call the original save method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.label}: {self.url}"

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from base.utils import compress_image
from tinymce import models as tinymce_models


class ProductVolume(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            help_text='Example: 1L, 4L, etc.')

    class Meta:
        verbose_name = 'Volume'
        verbose_name_plural = 'Volumes'

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    image = models.ImageField(upload_to='vehicles/')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        unique_together = ['make', 'model']

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(
                self.image, max_size=1400, format='PNG')
        # Call the original save method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.make} {self.model}"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Product Name")
    slug = models.SlugField(max_length=255, unique=True, blank=True,
                            help_text="IMPORTANT for product URL, QR code.")
    categories = models.ManyToManyField(
        Category, related_name='products', blank=True)
    volumes = models.ManyToManyField(
        ProductVolume,
        related_name='product_volumes',
        blank=True,
    )
    description = tinymce_models.HTMLField(default='')
    data_sheet = models.FileField(
        upload_to='product_data_sheets/', blank=True, null=True)
    standards_and_approval = tinymce_models.HTMLField(default='')
    suitable_vehicles = models.ManyToManyField(
        'Vehicle',
        related_name='suitable_products',
        blank=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name', 'id']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to automatically generate a slug 
        from the product name if a slug does not already exist.
        """
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class ProductDetailsItem(models.Model):
    name = models.CharField(max_length=255, default='')
    value = models.CharField(max_length=255, default='')
    for_product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Product Details'
        verbose_name_plural = 'Product Details'

    def __str__(self):
        return f"{self.name} - {self.value} - {self.for_product.name}"


class ProductImage(models.Model):
    image = models.ImageField(
        upload_to='uploads/products/', null=True, blank=True)
    alt = models.CharField(max_length=255, null=True, blank=True)
    for_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    for_volume = models.ForeignKey(ProductVolume, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(
                self.image, max_size=1400, format='PNG')
        # Call the original save method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.for_product.name} - {self.for_volume}"


class ProductInstruction(models.Model):
    instruction_steps = models.TextField(
        verbose_name='Instruction Steps (Text)')
    pdf_manual = models.FileField(
        upload_to='product_manuals/', blank=True, null=True)
    youtube_embed_url = models.URLField(max_length=200, blank=True, null=True)
    for_product = models.OneToOneField(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Product Instruction'
        verbose_name_plural = 'Product Instructions'

    def __str__(self):
        return f"Instruction Manual - #{self.id}"

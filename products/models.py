from django.db import models
from django.db.models import Min, Max
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
        through='ProductVariant',  # intermediary model
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

    def get_price_display(self):
        """
        Returns a string representing the price or price range.
        Examples: "$10.00", "$10.00 - $50.00", or "Price N/A"
        """
        # Aggregate finds the min and max price across all related variants
        prices = self.variants.aggregate(
            min_price=Min('price'),
            max_price=Max('price')
        )

        if prices['min_price'] is None:
            return "Price N/A"

        if prices['min_price'] == prices['max_price']:
            return f"${prices['min_price']:.2f}"

        return f"${prices['min_price']:.2f} - ${prices['max_price']:.2f}"

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


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='variants')
    volume = models.ForeignKey(ProductVolume, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'Product Variant (volume & price)'
        verbose_name_plural = 'Product Variants (volume & price)'
        # one product cannot have two prices for the same volume
        unique_together = ('product', 'volume')

    def __str__(self):
        return f"{self.product.name} - {self.volume.name} (${self.price})"


class ProductDetailsItem(models.Model):
    name = models.CharField(max_length=255, default='')
    value = models.CharField(max_length=255, default='')
    for_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='detail_items')

    class Meta:
        verbose_name = 'Product Details'
        verbose_name_plural = 'Product Details'

    def __str__(self):
        return f"{self.name} - {self.value} - {self.for_product.name}"


class ProductImage(models.Model):
    image = models.ImageField(
        upload_to='uploads/products/', null=True, blank=True)
    alt = models.CharField(max_length=255, null=True, blank=True)
    for_product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    for_volume = models.ForeignKey(
        ProductVolume, on_delete=models.CASCADE, related_name='volumes')

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
    for_product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='instructions')

    class Meta:
        verbose_name = 'Product Instruction'
        verbose_name_plural = 'Product Instructions'

    def __str__(self):
        return f"Instruction Manual - #{self.id}"

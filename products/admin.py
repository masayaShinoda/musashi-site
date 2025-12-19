from django.contrib import admin
from .models import Category, ProductInstruction, ProductDetailsItem, ProductVolume, Vehicle, Product, ProductImage, ProductVariant
from unfold.admin import ModelAdmin, TabularInline
from .forms import ProductAdminForm, ProductInstructionAdminForm


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    pass


# class CategoryInline(TabularInline):
#     model = Category
#     extra = 1
#     tab = True


class ProductDetailsItemInline(TabularInline):
    model = ProductDetailsItem
    extra = 1
    tab = True


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1
    tab = True


class ProductInstructionInline(TabularInline):
    model = ProductInstruction
    extra = 0
    tab = True
    form = ProductInstructionAdminForm


class ProductVariantInline(TabularInline):
    model = ProductVariant
    extra = 1
    tab = True
    verbose_name = "Price & Volume"
    verbose_names = "Prices & Volumes"


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    inlines = [ProductVariantInline, ProductImageInline,
               ProductDetailsItemInline, ProductInstructionInline]
    filter_horizontal = ('categories', 'suitable_vehicles')
    list_display = ['name', 'get_price_display', 'slug', 'id']
    # Optional: Give the column a nice name in the admin header

    def get_price_display(self, obj):
        return obj.get_price_display()
    get_price_display.short_description = "Price"

    readonly_fields = ['date_modified', 'date_created']
    ordering = ['-date_modified', 'name', 'id']
    form = ProductAdminForm


@admin.register(ProductVolume)
class ProductVolumeAdmin(ModelAdmin):
    list_display = ['name', 'id']
    ordering = ['name', 'id']


@admin.register(Vehicle)
class VehicleAdmin(ModelAdmin):
    list_display = ['make', 'model']
    ordering = ['make', 'model']

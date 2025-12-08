from django.contrib import admin
from .models import Category, ProductInstruction, ProductDetailsItem, ProductVolume, Vehicle, Product, ProductImage
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


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    inlines = [ProductImageInline,
               ProductDetailsItemInline, ProductInstructionInline]
    filter_horizontal = ('volumes', 'categories', 'suitable_vehicles')
    list_display = ['name', 'slug', 'price', 'id']
    readonly_fields = ['date_modified', 'date_created']
    ordering = ['-date_modified', 'name', 'id']
    form = ProductAdminForm


@admin.register(ProductVolume)
class ProductVolume(ModelAdmin):
    list_display = ['name', 'id']
    ordering = ['name', 'id']


@admin.register(Vehicle)
class VehicleAdmin(ModelAdmin):
    list_display = ['make', 'model']
    ordering = ['make', 'model']

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('<slug:product_slug>', views.product_details, name='product_details'),
]

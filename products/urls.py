from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('<slug:product_slug>', views.product, name='product'),
    path('<slug:product_slug>/place-order/',
         views.place_order_modal, name='place_order'),
]

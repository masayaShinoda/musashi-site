from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('<slug:product_slug>', views.product, name='product'),
    path('cart/add/<int:variant_id>/', views.cart_add, name='cart_add'),
    path('cart/add/<int:variant_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:variant_id>/',
         views.cart_remove, name='cart_remove'),
    path('cart/update/<int:variant_id>/',
         views.cart_update, name='cart_update'),
    path('checkout/', views.checkout, name='checkout'),
]

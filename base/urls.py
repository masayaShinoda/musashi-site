from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('links', views.links_page, name='links'),
]

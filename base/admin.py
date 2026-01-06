from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.models import Group
from .models import LinkPageDescription, Link
from .forms import LinkPageDescriptionAdminForm

# Register your models here.
admin.site.unregister(Group)


@admin.register(LinkPageDescription)
class LinkPageDescriptionAdmin(ModelAdmin):
    form = LinkPageDescriptionAdminForm


@admin.register(Link)
class LinkAdmin(ModelAdmin):
    list_display = ['label', 'url']

# ruff: noqa
from django.contrib import admin

from .models import Chemogene

# Register your models here.


@admin.register(Chemogene)
class ListingAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Chemogene._meta.fields]

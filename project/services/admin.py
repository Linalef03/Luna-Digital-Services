from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price_from', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {"slug": ("name",)}

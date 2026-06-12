from django.contrib import admin
from .models import Kliente, Notifikasaun

@admin.register(Kliente)
class KlienteAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

@admin.register(Notifikasaun)
class NotifikasaunAdmin(admin.ModelAdmin):
    list_display = ('kliente', 'type', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('message', 'kliente__name')

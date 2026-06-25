from django.contrib import admin
from .models import Kliente, Notifikasaun

@admin.register(Kliente)
class KlienteAdmin(admin.ModelAdmin):
    list_display = ('naran', 'email')
    search_fields = ('naran', 'email')

@admin.register(Notifikasaun)
class NotifikasaunAdmin(admin.ModelAdmin):
    list_display = ('kliente', 'tipu', 'created_at')
    list_filter = ('tipu', 'created_at')
    search_fields = ('mensajen', 'kliente__naran')

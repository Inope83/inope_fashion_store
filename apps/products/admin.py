from django.contrib import admin
from .models import Kategoria, Produtu

@admin.register(Kategoria)
class KategoriaAdmin(admin.ModelAdmin):
    list_display = ('naran',)
    search_fields = ('naran',)

@admin.register(Produtu)
class ProdutuAdmin(admin.ModelAdmin):
    list_display = ('naran', 'preco', 'stok', 'kategoria')
    list_filter = ('kategoria',)
    search_fields = ('naran', 'deskrisaun')

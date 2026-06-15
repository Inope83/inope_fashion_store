from django.contrib import admin
from .models import Kategoria, Produtu, ProdutuImage

class ProdutuImageInline(admin.TabularInline):
    model = ProdutuImage
    extra = 1

@admin.register(Kategoria)
class KategoriaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Produtu)
class ProdutuAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'kategoria')
    list_filter = ('kategoria',)
    search_fields = ('name', 'description')
    inlines = [ProdutuImageInline]

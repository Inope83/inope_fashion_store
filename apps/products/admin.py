from django.contrib import admin
from .models import Kategoria, Produtu, ProdutuImage

class ProdutuImageInline(admin.TabularInline):
    model = ProdutuImage
    extra = 1

@admin.register(Kategoria)
class KategoriaAdmin(admin.ModelAdmin):
    list_display = ('naran',)
    search_fields = ('naran',)

@admin.register(Produtu)
class ProdutuAdmin(admin.ModelAdmin):
    list_display = ('naran', 'presu', 'estok', 'kategoria')
    list_filter = ('kategoria',)
    search_fields = ('naran', 'deskrisaun')
    inlines = [ProdutuImageInline]

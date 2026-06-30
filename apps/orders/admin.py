from django.contrib import admin
from .models import Pedidu, DetalloPedidu, Pagamentu

class DetalloPediduInline(admin.TabularInline):
    model = DetalloPedidu
    extra = 1

@admin.register(Pedidu)
class PediduAdmin(admin.ModelAdmin):
    list_display = ('id', 'kliente', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('kliente__naran',)
    inlines = [DetalloPediduInline]

@admin.register(Pagamentu)
class PagamentuAdmin(admin.ModelAdmin):
    list_display = ('pedidu', 'metodu', 'total', 'status', 'created_at')
    list_filter = ('status', 'metodu')

from django.contrib import admin
from apps.users.models import Admin

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('username',)
    search_fields = ('username',)

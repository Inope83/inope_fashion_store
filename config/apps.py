from django.apps import AppConfig


class ConfigConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'config'
    verbose_name = 'Konfigurasaun'

    def ready(self):
        from django.contrib import admin

        admin.site.site_header = 'Administra Inope Store'
        admin.site.site_title = 'Inope Store Administrasaun'
        admin.site.index_title = 'Painel Administrasaun'

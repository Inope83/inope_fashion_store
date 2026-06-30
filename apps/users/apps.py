from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'apps.users'
    verbose_name = 'Uzuáriu sira'

    def ready(self):
        import apps.users.signals  # noqa: F401

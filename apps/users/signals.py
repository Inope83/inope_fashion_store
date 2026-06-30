from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import Kliente


@receiver(user_logged_in)
def sync_kliente_session(sender, request, user, **kwargs):
    """Keep Kliente session in sync when logging in via Django/allauth (e.g. social login)."""
    if not user.email:
        return
    kliente, created = Kliente.objects.get_or_create(
        email=user.email,
        defaults={
            'naran': user.get_full_name() or user.username or user.email,
            'password': user.password,
        },
    )
    if not created and kliente.password != user.password:
        kliente.password = user.password
        kliente.save(update_fields=['password'])
    request.session['kliente_id'] = kliente.id
    request.session['kliente_naran'] = kliente.naran

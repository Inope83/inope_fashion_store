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
            'is_staff': user.is_superuser or user.is_staff,
        },
    )
    if not created:
        changed = False
        if kliente.password != user.password:
            kliente.password = user.password
            changed = True
        should_be_staff = user.is_superuser or user.is_staff
        if kliente.is_staff != should_be_staff:
            kliente.is_staff = should_be_staff
            changed = True
        if changed:
            kliente.save(update_fields=['password', 'is_staff'])
    request.session['kliente_id'] = kliente.id
    request.session['kliente_naran'] = kliente.naran

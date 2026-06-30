from django.shortcuts import render, redirect
from django.urls import reverse
from apps.products.models import Produtu
from apps.users.models import Kliente


def home_view(request):
    kliente_id = request.session.get('kliente_id')
    if kliente_id and Kliente.objects.filter(id=kliente_id, is_staff=True).exists():
        return redirect('dashboard:dashboard_home')
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:dashboard_home')
    return render(request, 'home/home.html', {
        'featured': Produtu.objects.prefetch_related('images').all()[:8],
    })
from django.shortcuts import render
from apps.products.models import Produtu, Kategoria


def home_view(request):
    return render(request, 'home/home.html', {
        'featured': Produtu.objects.prefetch_related('images').all()[:8],
        'nav_kategorias': Kategoria.objects.all(),
        'cart_count': 0,  # placeholder until cart app is wired up
    })
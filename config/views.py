from django.shortcuts import render
from apps.products.models import Produtu


def home_view(request):
    return render(request, 'home/home.html', {
        'featured': Produtu.objects.prefetch_related('images').all()[:8],
    })
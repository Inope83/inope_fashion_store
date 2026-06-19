from django.shortcuts import render, get_object_or_404
from .models import Produtu, Kategoria


def produtu_detail_view(request, pk):
    produtu = get_object_or_404(Produtu, pk=pk)
    return render(request, 'products/detail.html', {
        'produtu': produtu,
        'nav_kategorias': Kategoria.objects.all(),
        'cart_count': 0,
    })

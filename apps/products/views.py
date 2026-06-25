from django.shortcuts import render, get_object_or_404
from .models import Produtu, Kategoria


def produtu_list_view(request):
    kategoria_id = request.GET.get('kategoria')
    produtus = Produtu.objects.all()
    if kategoria_id:
        produtus = produtus.filter(kategoria_id=kategoria_id)
    return render(request, 'products/list.html', {
        'produtus': produtus,
        'kategorias': Kategoria.objects.all(),
    })


def produtu_detail_view(request, pk):
    produtu = get_object_or_404(Produtu, pk=pk)
    return render(request, 'products/detail.html', {
        'produtu': produtu,
    })

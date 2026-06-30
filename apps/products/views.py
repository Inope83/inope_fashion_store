from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Produtu, Kategoria


from django.core.paginator import Paginator


def produtu_list_view(request):
    kategoria_id = request.GET.get('kategoria')
    q = request.GET.get('q', '').strip()
    produtus = Produtu.objects.all()
    if kategoria_id:
        produtus = produtus.filter(kategoria_id=kategoria_id)
    if q:
        produtus = produtus.filter(Q(naran__icontains=q) | Q(deskrisaun__icontains=q))
    paginator = Paginator(produtus, 12)
    page = request.GET.get('page', 1)
    produtus = paginator.get_page(page)
    return render(request, 'products/list.html', {
        'produtus': produtus,
        'kategorias': Kategoria.objects.all(),
        'q': q,
    })


def produtu_detail_view(request, pk):
    produtu = get_object_or_404(Produtu, pk=pk)
    return render(request, 'products/detail.html', {
        'produtu': produtu,
    })

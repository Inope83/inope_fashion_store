from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Produtu, Kategoria


from django.core.paginator import Paginator


def produtu_list_view(request):
    kategoria_id = request.GET.get('kategoria')
    q = request.GET.get('q', '').strip()
    presu_min = request.GET.get('presu_min', '').strip()
    presu_max = request.GET.get('presu_max', '').strip()
    tamanho = request.GET.get('tamanho', '').strip()

    produtus = Produtu.objects.all().order_by('-id')
    if kategoria_id:
        produtus = produtus.filter(kategoria_id=kategoria_id)
    if q:
        produtus = produtus.filter(Q(naran__icontains=q) | Q(deskrisaun__icontains=q))
    if presu_min:
        produtus = produtus.filter(presu__gte=presu_min)
    if presu_max:
        produtus = produtus.filter(presu__lte=presu_max)
    if tamanho:
        produtus = produtus.filter(tamanho=tamanho)

    paginator = Paginator(produtus, 12)
    page = request.GET.get('page', 1)
    produtus = paginator.get_page(page)
    return render(request, 'products/list.html', {
        'produtus': produtus,
        'kategorias': Kategoria.objects.all(),
        'q': q,
        'presu_min': presu_min,
        'presu_max': presu_max,
        'tamanho': tamanho,
    })


def produtu_detail_view(request, pk):
    produtu = get_object_or_404(Produtu, pk=pk)
    return render(request, 'products/detail.html', {
        'produtu': produtu,
    })

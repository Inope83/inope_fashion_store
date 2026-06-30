from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.products.models import Produtu
from .models import Pedidu, DetalloPedidu, Pagamentu
from .forms import CheckoutForm


def checkout_view(request):
    kliente_id = request.session.get('kliente_id')
    if not kliente_id:
        return redirect('kliente_login')
    cart = request.session.get('cart', [])
    if not cart:
        return redirect('cart')

    resolved = []
    for item in cart:
        try:
            produtu = Produtu.objects.get(id=item['produtu_id'])
        except Produtu.DoesNotExist:
            messages.error(request, f'Produtu ho ID {item["produtu_id"]} la existe.')
            return redirect('cart')
        kantidade = item.get('kantidade', 1)
        if produtu.estok < kantidade:
            messages.error(request, f'Estok {produtu.naran} la to\'o (disponível: {produtu.estok}).')
            return redirect('cart')
        resolved.append((produtu, kantidade))

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            total = sum(p.presu * q for p, q in resolved)
            pedidu = form.save(commit=False)
            pedidu.kliente_id = kliente_id
            pedidu.total = total
            pedidu.save()

            for produtu, kantidade in resolved:
                DetalloPedidu.objects.create(
                    pedidu=pedidu,
                    produtu=produtu,
                    kantidade=kantidade,
                    subtotal=produtu.presu * kantidade,
                )
                Produtu.objects.filter(id=produtu.id).update(estok=models.F('estok') - kantidade)

            Pagamentu.objects.create(
                pedidu=pedidu,
                metodu='cod',
                total=total,
                status='pendente',
            )

            request.session['cart'] = []
            messages.success(request, 'Pedidu suksesu!')
            return redirect('order_history')
    else:
        form = CheckoutForm()
    items = []
    for produtu, kantidade in resolved:
        items.append({'produtu': produtu, 'kantidade': kantidade, 'subtotal': produtu.presu * kantidade})
    return render(request, 'orders/checkout.html', {'form': form, 'items': items, 'total': sum(p.presu * q for p, q in resolved)})


def order_history_view(request):
    kliente_id = request.session.get('kliente_id')
    if not kliente_id:
        return redirect('kliente_login')
    pedidus = Pedidu.objects.filter(kliente_id=kliente_id).order_by('-created_at')
    return render(request, 'orders/history.html', {'pedidus': pedidus})


def order_detail_view(request, pk):
    kliente_id = request.session.get('kliente_id')
    if not kliente_id:
        return redirect('kliente_login')
    pedidu = get_object_or_404(Pedidu, pk=pk)
    if pedidu.kliente_id != kliente_id:
        return redirect('order_history')
    return render(request, 'orders/detail.html', {'pedidu': pedidu})

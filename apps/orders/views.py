from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.products.models import Produtu
from .models import Pedidu
from .forms import CheckoutForm


def checkout_view(request):
    kliente_id = request.session.get('kliente_id')
    if not kliente_id:
        return redirect('login')
    cart = request.session.get('cart', [])
    if not cart:
        return redirect('cart')
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            pedidu = form.save(commit=False)
            pedidu.kliente_id = kliente_id
            pedidu.total = sum(Produtu.objects.get(id=i['produtu_id']).preco * i['kantidade']
                               for i in cart)
            pedidu.save()
            request.session['cart'] = []
            messages.success(request, 'Pedidu suksesu!')
            return redirect('order_history')
    else:
        form = CheckoutForm()
    return render(request, 'orders/checkout.html', {'form': form})


def order_history_view(request):
    kliente_id = request.session.get('kliente_id')
    if not kliente_id:
        return redirect('login')
    pedidus = Pedidu.objects.filter(kliente_id=kliente_id).order_by('-created_at')
    return render(request, 'orders/history.html', {'pedidus': pedidus})


def order_detail_view(request, pk):
    pedidu = get_object_or_404(Pedidu, pk=pk)
    return render(request, 'orders/detail.html', {'pedidu': pedidu})

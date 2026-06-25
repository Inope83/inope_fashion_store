from django.shortcuts import render, redirect
from django.contrib import messages
from apps.products.models import Produtu


def cart_view(request):
    cart = request.session.get('cart', [])
    items = []
    total = 0
    for item in cart:
        produtu = Produtu.objects.get(id=item['produtu_id'])
        subtotal = produtu.preco * item['kantidade']
        items.append({'produtu': produtu, 'kantidade': item['kantidade'], 'subtotal': subtotal})
        total += subtotal
    return render(request, 'cart/cart.html', {'items': items, 'total': total, 'cart_count': len(cart)})


def cart_add_view(request):
    produtu_id = int(request.POST.get('produtu_id'))
    kantidade = int(request.POST.get('kantidade', 1))
    cart = request.session.get('cart', [])
    for item in cart:
        if item['produtu_id'] == produtu_id:
            item['kantidade'] += kantidade
            break
    else:
        cart.append({'produtu_id': produtu_id, 'kantidade': kantidade})
    request.session['cart'] = cart
    messages.success(request, 'Aumenta ba kareta sasan')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def cart_remove_view(request, item_id):
    cart = request.session.get('cart', [])
    request.session['cart'] = [item for item in cart if item['produtu_id'] != item_id]
    return redirect('cart')

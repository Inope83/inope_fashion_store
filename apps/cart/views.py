from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from apps.products.models import Produtu


def cart_view(request):
    cart = request.session.get('cart', [])
    items = []
    total = 0
    valid_cart = []
    for item in cart:
        try:
            produtu = Produtu.objects.get(id=item['produtu_id'])
        except Produtu.DoesNotExist:
            continue
        kantidade = item.get('kantidade', 1)
        subtotal = produtu.presu * kantidade
        items.append({'produtu': produtu, 'kantidade': kantidade, 'subtotal': subtotal})
        total += subtotal
        valid_cart.append(item)
    if len(valid_cart) != len(cart):
        request.session['cart'] = valid_cart
    return render(request, 'cart/cart.html', {'items': items, 'total': total, 'cart_count': len(valid_cart)})


def cart_add_view(request):
    produtu_id = request.POST.get('produtu_id')
    kantidade = request.POST.get('kantidade', 1)
    try:
        produtu_id = int(produtu_id)
        kantidade = int(kantidade)
        if kantidade < 1:
            raise ValueError
        if not Produtu.objects.filter(id=produtu_id).exists():
            raise ValueError
    except (TypeError, ValueError):
        messages.error(request, 'Dadus la válidu.')
        return redirect('kareta')
    cart = request.session.get('cart', [])
    for item in cart:
        if item['produtu_id'] == produtu_id:
            item['kantidade'] += kantidade
            break
    else:
        cart.append({'produtu_id': produtu_id, 'kantidade': kantidade})
    request.session['cart'] = cart
    messages.success(request, 'Aumenta ba kareta sasan')
    return redirect(request.META.get('HTTP_REFERER', 'kareta'))


def cart_remove_view(request, item_id):
    cart = request.session.get('cart', [])
    request.session['cart'] = [item for item in cart if item['produtu_id'] != item_id]
    return redirect('kareta')


def cart_update_view(request):
    if request.method != 'POST':
        return redirect('kareta')
    produtu_id = request.POST.get('produtu_id')
    kantidade = request.POST.get('kantidade')
    try:
        produtu_id = int(produtu_id)
        kantidade = int(kantidade)
        if kantidade < 1:
            raise ValueError
        get_object_or_404(Produtu, id=produtu_id)
    except (TypeError, ValueError):
        messages.error(request, 'Dadus la válidu.')
        return redirect('kareta')
    cart = request.session.get('cart', [])
    for item in cart:
        if item['produtu_id'] == produtu_id:
            item['kantidade'] = kantidade
            break
    request.session['cart'] = cart
    return redirect('kareta')

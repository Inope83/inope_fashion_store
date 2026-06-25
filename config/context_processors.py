from apps.products.models import Kategoria


def global_context(request):
    cart = request.session.get('cart', [])
    return {
        'nav_kategorias': Kategoria.objects.all(),
        'cart_count': len(cart),
    }

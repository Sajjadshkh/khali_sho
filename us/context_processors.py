from .models import Cart

def cart_count(request):
    """Context processor برای نمایش تعداد آیتم‌های سبد خرید"""
    if request.session.session_key:
        try:
            cart = Cart.objects.get(session_key=request.session.session_key)
            return {'cart_count': cart.items.count()}
        except Cart.DoesNotExist:
            return {'cart_count': 0}
    return {'cart_count': 0} 
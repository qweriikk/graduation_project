from .models import CartItem

def cart_data(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart__user=request.user)
        cart_total = sum(item.product.price * item.quantity for item in cart_items)
        return {
            'cart_items': cart_items,
            'cart_total': cart_total
        }
    return {
        'cart_items': [],
        'cart_total': 0
    }
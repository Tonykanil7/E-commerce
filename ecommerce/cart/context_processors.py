from cart.models import Cart

def count_items(request):
    user = request.user
    count = 0
    if request.user.is_authenticated:
        c = Cart.objects.filter(user=user)
        for i in c:
            count += i.quantity
    return {'count':count}
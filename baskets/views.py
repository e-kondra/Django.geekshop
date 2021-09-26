from django.shortcuts import render, HttpResponseRedirect
from mainapp.models import Product
from baskets.models import Basket

# Create your views here.
def basket_add(request, product_id):
    user_selected = request.user
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=user_selected, product=product)
    if not baskets.exists():
        Basket.objects.create(user=user_selected, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # переход туда где мы уже находимся

def basket_remove(request, basket_id):
    Basket.objects.get(id=basket_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # переход туда где мы уже находимся


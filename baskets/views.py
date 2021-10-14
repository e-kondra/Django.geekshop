from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView
from django.views.generic.edit import BaseDeleteView, UpdateView

from geekshop.mixin import LoginsRequiredMixin
from mainapp.models import Product
from baskets.models import Basket


class BasketCreateView(CreateView, LoginsRequiredMixin):
    model = Basket
    success_url = reverse_lazy('users:profile')
    context_object_name = 'baskets'
    fields = ['products']

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('pk', None)
        product = Product.objects.get(id=product_id)
        baskets = Basket.objects.filter(user=request.user, product=product)
        if not baskets.exists():
            Basket.objects.create(user=request.user, product=product, quantity=1)
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()

        context = {
            'products': Product.objects.filter()
        }
        result = render_to_string('mainapp/products_list.html', context, request=request)

        return JsonResponse({'result': result})


#
# @login_required
# def basket_add(request, product_id):
#     if request.is_ajax():
#         user_selected = request.user
#         product = Product.objects.get(id=product_id)
#         baskets = Basket.objects.filter(user=user_selected, product=product)
#         if not baskets.exists():
#             Basket.objects.create(user=user_selected, product=product, quantity=1)
#         else:
#             basket = baskets.first()
#             basket.quantity += 1
#             basket.save()
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # переход туда где мы уже находимся


class BasketDeleteView(DeleteView):
    model = Basket
    template_name = 'users/profile.html'


@login_required
def basket_remove(request, pk):
    Basket.objects.get(id=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # переход туда где мы уже находимся

#
# @login_required
# def basket_edit(request, pk, quantity):
#     if request.is_ajax():
#         basket = Basket.objects.get(id=pk)
#         if quantity > 0:
#             basket.quantity = quantity
#             basket.save()
#         else:
#             basket.delete()
#         baskets = Basket.objects.filter(user=request.user)
#         context = {
#             'baskets': baskets
#         }
#         result = render_to_string('baskets/baskets.html', context)
#         return JsonResponse({'result': result})
#

class BasketUpdateView(UpdateView, LoginsRequiredMixin):
    model = Basket
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    context_object_name = 'baskets'
    fields = ['products']

    def get_context_data(self, *args, **kwargs):
        context = super(BasketUpdateView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

    def get(self, request, *args, **kwargs):
        super(BasketUpdateView, self).get(request, *args,**kwargs)
        basket_id = self.kwargs.get('pk', None)
        quantity = self.kwargs.get('quantity', None)

        if request.is_ajax():
            basket = Basket.objects.get(id=basket_id)
            if quantity > 0:
                basket.quantity = quantity
                basket.save()
            else:
                basket.delete()
            context = {
                'baskets': Basket.objects.filter(user=self.request.user)
            }
            result = render_to_string('baskets/baskets.html', context, request=request)

            return JsonResponse({'result': result})
        return redirect(self.success_url)

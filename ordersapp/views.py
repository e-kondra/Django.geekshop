from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from baskets.models import Basket
from geekshop.mixin import BaseClassContextMixin
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)


class OrderCreateView(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop | Создать заказ'

        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1) #Создаем набор форм(главная мадель, подчиненная, используемая форма и сколько пустых строк)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items:
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=basket_items.count())
                formset = OrderFormSet()

                #добавляем на форму товары из баскета
                for num,form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                basket_items.delete()
            else:
                formset = OrderFormSet()

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic(): # используем транзакцию, чтобы заказ либо был полностью сохранен (либо чтобы его совсем не было)
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid(): # orderitems - это форма у нас
                orderitems.instance = self.object
                orderitems.save()

            if self.object.get_total_cost() == 0: # удалим пустой заказ
                self.object.delete()

        return super(OrderCreateView, self).form_valid(form)

class OrderUpdateView(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop | Изменить заказ'

        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if self.object.get_total_cost() == 0:
                self.object.delete()
        return super(OrderUpdateView, self).form_valid(form)

class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:list')


class OrderDetailView(DetailView, BaseClassContextMixin):
    model = Order
    title = 'GeekShop | Просмотр заказа'


def order_forming_complete(request, pk): # метод формирования статуса
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SEND_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('orders:list'))

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from ordersapp.models import Order


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user,is_active=True)


class OrderCreateView(CreateView):
    pass
class OrderUpdateView(UpdateView):
    pass
class OrderDeleteView(DeleteView):
    pass
class OrderDetailView(DetailView):
    pass

def order_forming_complete(request,pk):
    pass

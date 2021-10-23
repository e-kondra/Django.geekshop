from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView


class OrderListView(ListView):
    pass
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

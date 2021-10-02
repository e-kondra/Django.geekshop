from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


def index(request):
    return render(request, 'admins/admin.html')

class UserListView(ListView):
    pass

class UserCreateView(CreateView):
    pass

class UserUpdateView(UpdateView):
    pass

class UserDeleteView(DeleteView):
    pass
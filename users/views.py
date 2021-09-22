from django.shortcuts import render
from users.forms import UserLoginForm

# Create your views here.
def login(request):
    form = UserLoginForm()
    context = {
        'title': 'Geekshop - Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)

def register(request):
    context = {
        'title': 'Geekshop - Регистрация',
    }
    return render(request, 'users/register.html', context)
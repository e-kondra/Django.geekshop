from django.shortcuts import render

# Create your views here.
def login(request):
    context = {
        'title': 'Geekshop - Авторизация'
    }
    return render(request, 'users/login.html', context)

def register(request):
    context = {
        'title': 'Geekshop - Регистрация'
    }
    return render(request, 'users/register.html', context)
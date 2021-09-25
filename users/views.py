from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
import django.contrib.messages as messages

# Create your views here.
from users.forms import UserLoginForm, UserRegisterForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user.is_active:
                auth.login(request, user)  # авторизовываем
                return HttpResponseRedirect(
                    reverse('index'))  # перенаправление :reverse('index') - путь до страницы сайта index
    else:
        form = UserLoginForm()  # если форма невалидна, возвращаем пустую форму в контекст

    context = {
        'title': 'Geekshop - Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Регистрация успешна!')
            return HttpResponseRedirect(
                reverse('users:login'))  # перенаправление :reverse('index') - путь до страницы сайта входа пользователя
        # else:
        #     print(form.errors)  # ошибки формы теперь обрабатываем в html через динамич.шаблоны
    else:
        form = UserRegisterForm()  # если форма невалидна, возвращаем пустую форму в контекст
    context = {
        'title': 'Geekshop - Регистрация',
        'form': form
    }
    return render(request, 'users/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

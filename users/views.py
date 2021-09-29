from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
import django.contrib.messages as messages
# from django.contrib.messages import constants as messages

# Create your views here.
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from baskets.models import Basket


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
            messages.success(request, 'Регистрация успешна!')
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

@login_required
def profile(request):
    if request.method == 'POST':  # пост-запрос на сохранение измененных данных
        form = UserProfileForm(data=request.POST,
                               instance=request.user,  # в параметре instance передаем какого юзера обновлять
                               files=request.FILES)  # указываем, что необходимо сохранять и файлы
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные успешно изменены!')
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            messages.error(request, form.errors)

    baskets = Basket.objects.filter(user=request.user)
    context = {
        'title': 'Geekshop - Профайл',
        'form': UserProfileForm(instance=request.user),  # параметр instance позволяет передать данные из пользователя
        'baskets': baskets,
        # Это способ для подсчет сумм из view (но лучше из baskets.model.py, так как память надо во вью экономить, поэтому этот оставляю как пример)
        # 'total_quantity': sum(basket.quantity for basket in baskets),
        # 'total_sum': sum(basket.sum() for basket in baskets)
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

def total_quantity(request):
    pass
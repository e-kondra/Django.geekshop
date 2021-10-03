from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm
from geekshop.mixin import CustomDispatchMixin
from users.models import User


def index(request):
    return render(request, 'admins/admin.html')


class UserListView(ListView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-read.html'  # шаблон, кот. используем
    # context_object_name = 'users' если задать тут эту переменную, в шаблоне можно будет к ней обращаться, другой вариант - сейчас в шаблоне

    def get_context_data(self, *, object_list=None,
                         **kwargs):  # ф-я вызывается до template, сможет передать данные в шаблон
        # получает весь контекст
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Пользователи'  # и так можно любую переменную отсюда передать в щаблон
        return context


class UserCreateView(CreateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm  # какую форму используем(не вызываем, а просто передаем)
    success_url = reverse_lazy('admins:admins_user')  # куда перенаправить в случае успеха

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Регистрация'
        return context


class UserUpdateView(UpdateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Обновление пользователя'
        return context

class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admins_user')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object() # объект с переданным pk получен
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url()) # перенаправление в success_url

from django.db.models import F
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db import connection

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, CategoryAdminCreateForm, CategoryAdminUpdateForm, \
    ProductAdminRegisterForm, ProductAdminUpdateForm
from geekshop.mixin import CustomDispatchMixin
from mainapp.models import ProductCategory, Product
from users.models import User


def index(request):
    return render(request, 'admins/admin.html')

def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]

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

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Регистрация'
        return context


class UserUpdateView(UpdateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self,*, object_list=None, **kwargs):
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


class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'admins/admin-category-read.html'
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Категории'
        return  context


class CategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'admins/admin-category-create.html'
    success_url = reverse_lazy('admins:admins_categories')
    form_class = CategoryAdminCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Создание категории'
        return context


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'admins/admin-category-update-delete.html'
    success_url = reverse_lazy('admins:admins_categories')
    form_class = CategoryAdminUpdateForm

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(CategoryUpdateView, self).get_context_data(**kwargs)
    #     context['title'] = 'Админка | Изменение категории'
    #     return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                print(f'применяется скидка {discount} % к товарам категории {self.object.name}')
                self.object.product_set.update(price=F('price')*(1-discount/100))
                db_profile_by_type(self.__class__,'UPDATE',connection.queries)
        return HttpResponseRedirect(self.get_success_url())

class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'admins/admin-category-update-delete.html'
    success_url = reverse_lazy('admins:admins_categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.product_set.update(is_active=False) # изменяем все продукты с помощью product_set
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductListView(ListView):
    model = Product
    template_name = 'admins/admin-product-read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all().select_related()
        context['title'] = 'Админка | Продукты'
        return context

class ProductCreateView(CreateView):
    model = Product
    template_name = 'admins/admin-product-create.html'
    form_class = ProductAdminRegisterForm  # какую форму используем
    success_url = reverse_lazy('admins:admins_products')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Создание продукта'
        context['categories'] = ProductCategory.objects.all().select_related()
        return context


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'admins/admin-product-update-delete.html'
    success_url = reverse_lazy('admins:admins_products')
    form_class = ProductAdminUpdateForm

    def get_context_data(self,*, object_list=None, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Изменение продукта'
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'admins/admin-product-update-delete.html'
    success_url = reverse_lazy('admins:admins_products')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

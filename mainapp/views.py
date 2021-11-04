from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
import datetime
import os, json

from django.urls import reverse_lazy
from django.views.generic import ListView
from django.conf import settings
from django.core.cache import cache

from geekshop.mixin import BaseClassContextMixin
from .models import Product,ProductCategory


MODULE_DIR = os.path.dirname(__file__)  # директория проекта


# Create your views here.
def index(request):
    context = {
        'date': datetime.date.today(),
        'title': 'geekshop',
    }
    return render(request, 'mainapp/index.html', context)

#  пишем категории в кеш
def get_link_category():
    if settings.LOW_CACHE:
        key = 'links_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategory.objects.all()
            cache.set(key, link_category)
        return link_category
    else:
        return ProductCategory.objects.all()


class ProductsListView(ListView, BaseClassContextMixin):
    model = Product
    template_name = 'mainapp/products.html'
    title = 'Каталог'
    success_url = reverse_lazy('mainapp:products')

    def get_queryset(self):
        category_id = self.kwargs.get('pk', None)
        self.products = Product.objects.filter(category_id=category_id).select_related('category') if category_id != None else Product.objects.all().select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['date'] = datetime.date.today()
        context['categories'] = get_link_category()

        page_id = self.kwargs.get('page_id', None)
        paginator = Paginator(self.products, per_page=3)
        try:
            products_paginator = paginator.page(page_id)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context['products'] = products_paginator
        return context


# def products(request, category_id=None, page_id=1):
#     #category_id - для фильтра передаем
#     # file_path = os.path.join(MODULE_DIR, 'fixtures/db.json')
#     products = Product.objects.filter(category_id=category_id) if category_id != None else Product.objects.all()
#
#     paginator = Paginator(products, per_page=3)
#     try:
#         products_paginator = paginator.page(page_id)
#     except PageNotAnInteger:
#         products_paginator = paginator.page(1)
#     except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages)
#
#     context = {
#         'title': 'Каталог',
#         'date': datetime.date.today(),
#         'products': products_paginator,
#         'categories': ProductCategory.objects.all() }
#     # context.update({'products': products_paginator}) - это другой вариант передачи значения в context
#         # загрузка из json
#         # 'products': json.load(open(file_path, encoding="utf-8")),
#         # заполнение вручную
#         # 'products_list': [
#         #    {'src': 'vendor/img/products/Adidas-hoodie.png',
#         #     'name': 'Худи черного цвета с монограммами adidas Originals',
#         #     'price': '6 090,00', 'description': 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.'},
#         # ],
#
#     return render(request, 'mainapp/products.html', context)

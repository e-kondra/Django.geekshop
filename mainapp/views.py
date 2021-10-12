from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
import datetime
import os, json

from django.urls import reverse_lazy
from django.views.generic import ListView

from .models import Product,ProductCategory


MODULE_DIR = os.path.dirname(__file__)  # директория проекта


# Create your views here.
def index(request):
    context = {
        'date': datetime.date.today(),
        'title': 'geekshop',
    }
    return render(request, 'mainapp/index.html', context)


class ProductsListView(ListView):
    model = Product
    template_name = 'mainapp/products.html'
    success_url = reverse_lazy('mainapp:products')

    def get_queryset(self):
        category_id = self.kwargs.get('pk', None)
        self.products = Product.objects.filter(category_id=category_id) if category_id != None else Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['date'] = datetime.date.today()
        context['categories'] = ProductCategory.objects.all()

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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
import datetime
import os, json

from .models import Product,ProductCategory


MODULE_DIR = os.path.dirname(__file__)  # директория проекта


# Create your views here.
def index(request):
    context = {
        'date': datetime.date.today(),
        'title': 'geekshop',
    }
    return render(request, 'mainapp/index.html', context)


def products(request, category_id=None, page_id=1):
    #category_id - для фильтра передаем
    # file_path = os.path.join(MODULE_DIR, 'fixtures/db.json')
    products = Product.objects.filter(category_id=category_id) if category_id != None else Product.objects.all()

    paginator = Paginator(products, per_page=3)
    try:
        products_paginator = paginator.page(page_id)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': 'Каталог',
        'date': datetime.date.today(),
        'products': products_paginator,
        'categories': ProductCategory.objects.all() }
    # context.update({'products': products_paginator}) - это другой вариант передачи значения в context
        # загрузка из json
        # 'products': json.load(open(file_path, encoding="utf-8")),
        # заполнение вручную
        # 'products_list': [
        #    {'src': 'vendor/img/products/Adidas-hoodie.png',
        #     'name': 'Худи черного цвета с монограммами adidas Originals',
        #     'price': '6 090,00', 'description': 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.'},
        # ],

    return render(request, 'mainapp/products.html', context)

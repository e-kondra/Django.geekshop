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


def products(request, category_id=None):
    #category_id - для фильтра передаем
    # file_path = os.path.join(MODULE_DIR, 'fixtures/db.json')
    products = Product.objects.filter(category_id=category_id) if category_id != None else Product.objects.all()

    context = {
        'title': 'products',
        'date': datetime.date.today(),
        'products': products,
        'categories': ProductCategory.objects.all(),
        # загрузка из json
        # 'products': json.load(open(file_path, encoding="utf-8")),
        # заполнение вручную
        # 'products_list': [
        #    {'src': 'vendor/img/products/Adidas-hoodie.png',
        #     'name': 'Худи черного цвета с монограммами adidas Originals',
        #     'price': '6 090,00', 'description': 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.'},
        #    {'src': 'vendor/img/products/Blue-jacket-The-North-Face.png',
        #     'name': 'Синяя куртка The North Face', 'price': '23 725,00',
        #     'description': 'Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.'},
        #    {'src': 'vendor/img/products/Brown-sports-oversized-top-ASOS-DESIGN.png',
        #     'name': 'Коричневый спортивный oversized-топ ASOS DESIGN',
        #     'price': '3 390,00', 'description': 'Материал с плюшевой текстурой. Удобный и мягкий.'},
        #    {'src': 'vendor/img/products/Black-Nike-Heritage-backpack.png',
        #     'name': 'Черный рюкзак Nike Heritage',
        #     'price': '2 340,00', 'description': 'Плотная ткань. Легкий материал.'},
        #    {'src': 'vendor/img/products/Black-Dr-Martens-shoes.png',
        #     'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex',
        #     'price': '13 590,00', 'description': 'Гладкий кожаный верх. Натуральный материал.'},
        #    {'src': 'vendor/img/products/Dark-blue-wide-leg-ASOs-DESIGN-trousers.png',
        #     'name': 'Темно-синие широкие строгие брюки ASOS DESIGN',
        #     'price': '2 890,00', 'description': 'Легкая эластичная ткань сирсакер Фактурная ткань.'},
        # ],
    }
    return render(request, 'mainapp/products.html', context)

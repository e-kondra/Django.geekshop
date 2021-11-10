from django.test.client import Client
from django.test import TestCase

# Create your tests here.
from mainapp.models import ProductCategory, Product


class TestMainSmokeTest(TestCase):
    status_code_success = 200
    # 1. предустановленные параметры(создаем категорию и продукт)
    def setUp(self) -> None:
        category = ProductCategory.objects.create(name='Test')
        Product.objects.create(category=category, name='product_test', price=100)
        Product.objects.create(category=category, name='product_test2', price=120)

        self.client = Client()

    # 2.  Выполнение теста
    def test_products_pages(self):
        response = self.client.get('/')  # идем на главную страницу
        self.assertEqual(response.status_code, self.status_code_success) # проверяем код с которым она выполнилас

    def test_products_product(self):
        for product_item in Product.objects.all():
            response = self.client.get(f'/products/detail/{product_item.pk}/')
            self.assertEqual(response.status_code, self.status_code_success)

    def test_products_basket(self):
        response = self.client.get(f'/users/profile/')
        self.assertEqual(response.status_code, 302)

    # определяется для очистки после работы теста
    def tearDown(self) -> None:
        pass


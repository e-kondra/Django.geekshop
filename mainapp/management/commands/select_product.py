from django.core.management import BaseCommand
from django.db import connection
from django.db.models import Q

from admins.views import db_profile_by_type
from mainapp.models import Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        products = Product.objects.filter(Q(category__name='Обувь') | Q(category__name='Одежда'))
        print(products)
        db_profile_by_type('learn db','',connection.queries)
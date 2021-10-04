from django.contrib import admin
from mainapp.models import ProductCategory,Product


# Register your models here.
admin.site.register(ProductCategory)
# admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category') # список колонок для вывода в табличке
    fields = ('name', 'image', ('price', 'quantity'),'description', 'category' ) # поля в описании продукта
    readonly_fields = ('description',)
    ordering = ('name', 'price')
    search_fields = ('name',)
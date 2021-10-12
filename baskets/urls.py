
from django.urls import path

from baskets.views import  BasketCreateView, basket_remove,  basket_edit, BasketDeleteView
# from baskets.views import basket_add, BasketUpdateView,BasketDeleteView

app_name = 'baskets'

urlpatterns = [
    path('add/<int:pk>/', BasketCreateView.as_view(), name='basket'),
     path('remove/<int:pk>/', basket_remove, name='basket_remove'),
    # path('remove/<int:pk>/', BasketDeleteView.as_view(), name='basket_remove'),
    path('edit/<int:pk>/<int:quantity>/', basket_edit, name='basket_edit')
]

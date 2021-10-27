"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include


from .views import OrderListView, OrderCreateView, OrderDeleteView, OrderUpdateView, OrderDetailView, \
    order_forming_complete, payment_result, get_product_price

from mainapp.views import index

app_name = 'ordersapp'

urlpatterns = [
    path('', OrderListView.as_view(), name='list'), # по ссылке Order мы попадем в OrderList
    path('create/',OrderCreateView.as_view(),name='create'),
    path('update/<int:pk>/',OrderUpdateView.as_view(),name='update'),
    path('delete/<int:pk>/',OrderDeleteView.as_view(),name='delete'),
    path('read/<int:pk>/',OrderDetailView.as_view(),name='read'),
    path('forming_complete/<int:pk>/',order_forming_complete,name='forming_complete'),

    path('product/<int:pk>/price/', get_product_price, name='product_price'),
    path('payment/result/',payment_result,name='payment_result'),

]

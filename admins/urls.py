
from django.urls import path
from .views import index, UserCreateView, UserListView, UserDeleteView, UserUpdateView



app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admins_user'),
    path('users-create/', UserCreateView.as_view(), name='admins_user_create'),
    path('user-update/<int:pk>/',UserUpdateView.as_view(), name='admins_user_update'),
    path('user-delete/<int:pk>/', UserDeleteView.as_view(), name='admins_user_delete'),
    # path('add/<int:product_id>/', basket_add, name='basket'),

]

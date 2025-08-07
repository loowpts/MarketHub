from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),
    path('create/', views.order_create, name='order_create'),
    path('list/', views.order_list, name='order_list'),
]

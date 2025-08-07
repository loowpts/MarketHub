from django.urls import path
from . import views

app_name = 'shops'

urlpatterns = [
    path('', views.shop_list, name='shop_list'),
    path('create/', views.shop_create, name='shop_create'),
    path('<int:pk>/', views.shop_detail, name='shop_detail'),
    path('moderate/<int:pk>/', views.moderate_shop, name='moderate_shop'),
    path('<int:pk>/edit/', views.shop_edit, name='shop_edit'),
]

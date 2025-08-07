from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create/<int:product_id>/', views.review_create, name='review_create'),
    path('shop/create/<int:shop_id>/', views.shop_review_create, name='shop_review_create'),
]

from django.contrib import admin
from .models import Review, ShopReview

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    search_fields = ('user__email', 'product__name', 'comment')
    list_filter = ('rating', 'created_at')

@admin.register(ShopReview)
class ShopReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'shop', 'rating', 'created_at')
    search_fields = ('user__email', 'shop__name', 'comment')
    list_filter = ('rating', 'created_at')

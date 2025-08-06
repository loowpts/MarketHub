from django.contrib import admin
from .models import Shop, ShopModerationRequest

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'created_at', 'rating')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'owner__username')
    readonly_fields = ('rating',)
    ordering = ('-created_at',)

@admin.register(ShopModerationRequest)
class ShopModerationRequestAdmin(admin.ModelAdmin):
    list_display = ('shop', 'moderator', 'status', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('shop__name', 'moderator__username')
    ordering = ('-submitted_at',)

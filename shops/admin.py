from django.contrib import admin
from .models import Shop, ShopModerationRequest
from users.models import User

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'created_at', 'rating')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'owner__email')
    ordering = ('-created_at',)

@admin.register(ShopModerationRequest)
class ShopModerationRequestAdmin(admin.ModelAdmin):
    list_display = ('shop', 'moderator', 'status', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('shop__name', 'moderator__email')
    ordering = ('-submitted_at',)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'moderator':
            kwargs['queryset'] = User.objects.filter(profile__role='admin')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

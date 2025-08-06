from django.contrib import admin
from .models import Product, ProductImage, Category

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image']
    readonly_fields = []
    can_delete = True

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'category', 'price', 'stock', 'created_at')
    list_filter = ('shop', 'category')
    search_fields = ('name', 'description', 'shop__name')
    ordering = ('-created_at',)
    inlines = [ProductImageInline]
    fieldsets = (
        (None, {
            'fields': ('shop', 'category', 'name', 'description', 'price', 'main_image', 'stock')
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)

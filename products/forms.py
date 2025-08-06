from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'main_image', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500',
                'placeholder': 'Название товара'
            }),
            'description': forms.Textarea(attrs={
                'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500',
                'placeholder': 'Описание товара',
                'rows': 4
            }),
            'category': forms.Select(attrs={
                'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500',
                'placeholder': 'Цена'
            }),
            'main_image': forms.FileInput(attrs={
                'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900',
                'accept': 'image/*'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500',
                'placeholder': 'Количество на складе'
            }),
        }
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'category': 'Категория',
            'price': 'Цена',
            'main_image': 'Основное изображение',
            'stock': 'Количество на складе',
        }

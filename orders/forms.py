from django import forms
from .models import CartItem

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500',
                'min': 1,
                'placeholder': 'Количество'
            }),
        }
        labels = {
            'quantity': 'Количество',
        }

from django import forms
from .models import Review, ShopReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500',
                'min': 1,
                'max': 5,
                'placeholder': 'Рейтинг (1-5)'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500',
                'rows': 4,
                'placeholder': 'Ваш комментарий'
            }),
        }
        labels = {
            'rating': 'Рейтинг',
            'comment': 'Комментарий',
        }

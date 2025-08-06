from django import forms
from .models import Shop, ShopModerationRequest
from users.models import User

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'description', 'logo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'logo': forms.FileInput(attrs={'accept': 'image/*'}),
        }

class ShopModerationForm(forms.ModelForm):
    class Meta:
        model = ShopModerationRequest
        fields = ['moderator', 'comment', 'status']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
            'status': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['moderator'].queryset = User.objects.filter(profile__role='admin')

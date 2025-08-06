from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.utils.html import strip_tags
from .models import User, UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        max_length=254,
        label="Электронная почта",
        widget=forms.EmailInput(attrs={
            'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500',
            'placeholder': 'Электронная почта'
        })
    )
    password1 = forms.CharField(
        required=True,
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500',
            'placeholder': 'Пароль'
        })
    )
    password2 = forms.CharField(
        required=True,
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={
            'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500',
            'placeholder': 'Повторите пароль'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот адрес уже используется.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(user=user)
        return user

class UserProfileForm(forms.ModelForm):
    phone = forms.CharField(
        required=False,
        label="Номер телефона",
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', "Введите корректный номер телефона.")],
        widget=forms.TextInput(attrs={
            'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500',
            'placeholder': 'Телефон'
        })
    )

    class Meta:
        model = UserProfile
        fields = (
            'first_name', 'last_name', 'phone',
            'address1', 'address2', 'city',
            'country', 'province'
        )
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'address1': 'Адрес (строка 1)',
            'address2': 'Адрес (строка 2)',
            'city': 'Город',
            'country': 'Страна',
            'province': 'Регион/Область',
            'phone': 'Телефон',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500', 'placeholder': 'Фамилия'}),
            'address1': forms.TextInput(attrs={'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500', 'placeholder': 'Адрес (строка 1)'}),
            'address2': forms.TextInput(attrs={'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500', 'placeholder': 'Адрес (строка 2)'}),
            'city': forms.TextInput(attrs={'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500', 'placeholder': 'Город'}),
            'country': forms.TextInput(attrs={'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500', 'placeholder': 'Страна'}),
            'province': forms.TextInput(attrs={'class': 'dotted-input w-full py-3 text-sm font-medium text-gray-900 placeholder-gray-500', 'placeholder': 'Регион / Область'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        for field in ['first_name', 'last_name', 'address1', 'address2', 'city', 'country', 'province', 'phone']:
            if cleaned_data.get(field):
                cleaned_data[field] = strip_tags(cleaned_data[field])
        return cleaned_data

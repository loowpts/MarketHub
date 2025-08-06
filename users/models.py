from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfile(models.Model):
    ROLE_CHOICES = (
    ('buyer', 'Покупатель'),
    ('seller', 'Продавец'),
    ('admin', 'Администратор'),
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    first_name = models.CharField("Имя", max_length=50, blank=True, null=True)
    last_name = models.CharField("Фамилия", max_length=50, blank=True, null=True)
    phone = models.CharField("Телефон", max_length=20, blank=True, null=True)
    company = models.CharField("Компания", max_length=255, blank=True, null=True)
    address1 = models.CharField("Адрес 1", max_length=255, blank=True, null=True)
    address2 = models.CharField("Адрес 2", max_length=255, blank=True, null=True)
    city = models.CharField("Город", max_length=255, blank=True, null=True)
    country = models.CharField("Страна", max_length=255, blank=True, null=True)
    province = models.CharField("Регион", max_length=100, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='buyer')

    def __str__(self):
        return f"{self.user.email} - Профиль"

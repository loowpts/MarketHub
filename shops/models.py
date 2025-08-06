from django.db import models
from django.core.exceptions import ValidationError
from users.models import User

class Shop(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидание'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shops',
        verbose_name='Владелец магазина'
    )
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    logo = models.ImageField(upload_to='shop_logo/', blank=True, null=True, verbose_name='Логотип')
    status = models.CharField(choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def update_rating(self):
        pass

    def clean(self):
        if self.owner.shops.exists() and not self.pk:
            raise ValidationError('Пользователь может создать только один магазин.')

    def __str__(self) -> str:
        return f'Магазин {self.name} - Владелец: {self.owner}'

class ShopModerationRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидание'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    )
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, verbose_name='Магазин')
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подачи')
    moderator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Модератор'
    )
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')
    status = models.CharField(choices=STATUS_CHOICES, default='pending', verbose_name='Статус')

    class Meta:
        verbose_name = 'Заявка на модерацию магазина'
        verbose_name_plural = 'Заявки на модерацию магазинов'
        ordering = ['-submitted_at']

    def __str__(self) -> str:
        return f'Заявка на модерацию для ({self.shop.name}) - статус: {self.status}'

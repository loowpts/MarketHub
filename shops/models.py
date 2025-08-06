from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


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
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to='shop_logo/', blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def update_rating(self):
        pass

    def __str__(self) -> str:
        return f'Магазин {self.name} - Владелец: {self.owner}'
    
    

class ShopModerationRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидание'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    )
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, verbose_name='Магазин')
    submitted_at = models.DateTimeField(auto_now_add=True)
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default='pending')

    class Meta:
        verbose_name = 'Заявка на модерацию магазина'
        verbose_name_plural = 'Заявки на модерацию магазинов'
        ordering = ['-submitted_at']

    def __str__(self) -> str:
        return f'Заявка на модерацию для ({self.shop.name}) - статус: {self.status}'

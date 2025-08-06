from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('shops/', include('shops.urls', namespace='shops')),
    path('products/', include('products.urls')),
    # path('orders/', include('orders.urls')),
    # path('reviews/', include('reviews.urls')),
    # path('chat/', include('chat.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

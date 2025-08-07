from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, UserProfileForm
from products.models import Product
from shops.models import Shop
from django.db.models import Sum
from .models import User


def index_view(request):
    top_shops = Shop.objects.filter(status='approved').annotate(
        total_orders=Sum('products__order_items__quantity')
    ).order_by('-total_orders')[:6]

    featured_shops = Shop.objects.filter(status='approved').order_by('-rating')[:6]

    products_count = Product.objects.filter(shop__status='approved').count()
    shops_count = Shop.objects.filter(status='approved').count()
    users_count = User.objects.filter(is_active=True).count()

    context = {
        'top_shops': top_shops,
        'featured_shops': featured_shops,
        'products_count': products_count,
        'shops_count': shops_count,
        'users_count': users_count,
    }
    return render(request, 'users/index.html', context)

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Успешная регистрация!')
            return redirect('users:index')
        else:
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Добро пожаловать на площадку!')
            return redirect('users:index')
        else:
            messages.error(request, 'Неверный email или пароль')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('users:index')

@login_required
def profile_view(request):
    profile = request.user.profile 
    form = UserProfileForm(instance=profile)
    return render(request, 'users/profile.html', {'profile': profile, 'form': form})

@login_required
def profile_edit_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('users:profile')
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'users/profile_edit.html', {'form': form})

@login_required
def become_seller(request):
    profile = request.user.profile
    if profile.role == 'seller':
        messages.error(request, 'Вы уже продавец.')
        return redirect('users:profile')
    if request.method == 'POST':
        profile.role = 'seller'
        profile.save()
        messages.success(request, 'Вы стали продавцом! Теперь вы можете создать магазин.')
        return redirect('users:profile')
    return render(request, 'users/become_seller.html', {})

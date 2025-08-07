from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Shop, ShopModerationRequest
from .forms import ShopForm, ShopModerationForm
from users.models import User

def shop_list(request):
    query = request.GET.get('q', '')
    shops = Shop.objects.filter(status='approved')
    if query:
        shops = shops.filter(name__icontains=query)
    return render(request, 'shops/shop_list.html', {'shops': shops, 'query': query})

def shop_detail(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    products = shop.products.filter(shop__status='approved').order_by('-created_at')
    return render(request, 'shops/shop_detail.html', {'shop': shop, 'products': products})

@login_required
def shop_create(request):
    if request.user.profile.role != 'seller':
        messages.error(request, 'Только продавцы могут создавать магазины.')
        return redirect('users:index')
    if request.user.shops.exists():
        messages.error(request, 'Вы уже создали магазин.')
        return redirect('users:profile')
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        shop = Shop(owner=request.user)
        form = ShopForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            shop = form.save()
            ShopModerationRequest.objects.create(shop=shop, status='pending')
            messages.success(request, 'Магазин создан и отправлен на модерацию.')
            return redirect('users:profile')
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = ShopForm()
    return render(request, 'shops/shop_form.html', {'form': form})


@login_required
def shop_edit(request, pk):
    shop = get_object_or_404(Shop, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Магазин обновлён.')
            return redirect('shops:shop_detail', pk=shop.pk)
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = ShopForm(instance=shop)
    return render(request, 'shops/shop_form.html', {'form': form, 'shop': shop})


@login_required
@user_passes_test(lambda u: u.profile.role == 'admin')
def moderate_shop(request, pk):
    moderation_request = get_object_or_404(ShopModerationRequest, pk=pk)
    if request.method == 'POST':
        form = ShopModerationForm(request.POST, instance=moderation_request)
        if form.is_valid():
            moderation_request = form.save(commit=False)
            moderation_request.moderator = request.user
            moderation_request.shop.status = form.cleaned_data['status']
            moderation_request.shop.save()
            moderation_request.save()
            messages.success(request, f'Магазин {moderation_request.shop.name} {moderation_request.status}.')
            return redirect('shops:shop_list')
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = ShopModerationForm(instance=moderation_request)
    return render(request, 'shops/moderate_shop.html', {'form': form, 'moderation_request': moderation_request})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Shop, ShopModerationRequest
from .forms import ShopForm, ShopModerationForm
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def shop_create(request):
    if request.user.profile.role != 'seller':
        messages.error(request, 'Только продавцы могут создавать магазины.')
        return redirect('users:index')
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            shop.status = 'pending'
            shop.save()
            ShopModerationRequest.objects.create(shop=shop)
            messages.success(request, 'Заявка успешно создана, мы вам сообщим, когда она будет рассмотрена.')
            return redirect('shops:shop_detail', pk=shop.pk)
    else:
        form = ShopForm()
    return render(request, 'shops/shop_form.html', {'form': form})

def shop_list(request):
    shops = Shop.objects.filter(status='approved').order_by('-created_at')
    return render(request, 'shops/shop_list.html', {'shops': shops})

def shop_detail(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if shop.status != 'approved':
        messages.info(request, 'Магазин находится на модерации и еще не одобрен.')
    return render(request, 'shops/shop_detail.html', {'shop': shop})

@login_required
def moderate_shop(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Только модераторы могут обрабатывать заявки.')
        return redirect('users:index')
    moderation_request = get_object_or_404(ShopModerationRequest, pk=pk)
    if request.method == 'POST':
        form = ShopModerationForm(request.POST, instance=moderation_request)
        if form.is_valid():
            form.save()
            shop = moderation_request.shop
            shop.status = form.cleaned_data['status']
            shop.save()
            messages.success(request, 'Заявка обработана.')
            return redirect('shops:shop_detail', pk=shop.pk)
    else:
        form = ShopModerationForm(instance=moderation_request)
    return render(request, 'shops/moderate_shop.html', {'form': form, 'shop': moderation_request.shop})

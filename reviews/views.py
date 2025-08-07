from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review, ShopReview
from .forms import ReviewForm
from products.models import Product
from shops.models import Shop

@login_required
def review_create(request, product_id):
    product = get_object_or_404(Product, pk=product_id, shop__status='approved')
    has_purchased = product.order_items.filter(order__user=request.user).exists()
    if not has_purchased:
        messages.error(request, 'Вы можете оставить отзыв только на купленные товары.')
        return redirect('products:product_detail', pk=product_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if Review.objects.filter(user=request.user, product=product).exists():
                messages.error(request, 'Вы уже оставили отзыв на этот товар.')
                return redirect('products:product_detail', pk=product_id)
            Review.objects.create(
                user=request.user,
                product=product,
                **form.cleaned_data
            )
            messages.success(request, 'Отзыв успешно добавлен.')
            return redirect('products:product_detail', pk=product_id)
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form, 'product': product})

@login_required
def shop_review_create(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id, status='approved')
    has_purchased = shop.products.filter(order_items__order__user=request.user).exists()
    if not has_purchased:
        messages.error(request, 'Вы можете оставить отзыв только на магазины, в которых покупали товары.')
        return redirect('shops:shop_detail', pk=shop_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if ShopReview.objects.filter(user=request.user, shop=shop).exists():
                messages.error(request, 'Вы уже оставили отзыв на этот магазин.')
                return redirect('shops:shop_detail', pk=shop_id)
            ShopReview.objects.create(
                user=request.user,
                shop=shop,
                **form.cleaned_data
            )
            messages.success(request, 'Отзыв успешно добавлен.')
            return redirect('shops:shop_detail', pk=shop_id)
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = ReviewForm()
    return render(request, 'reviews/shop_review_form.html', {'form': form, 'shop': shop})

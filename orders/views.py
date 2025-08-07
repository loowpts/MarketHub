from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem
from .forms import CartItemForm
from products.models import Product

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, shop__status='approved')
    cart, created = Cart.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity > product.stock:
                messages.error(request, 'Недостаточно товара на складе.')
                return render(request, 'orders/cart_add.html', {'form': form, 'product': product})
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart, product=product, defaults={'quantity': quantity}
            )
            if not item_created:
                cart_item.quantity += quantity
                if cart_item.quantity > product.stock:
                    messages.error(request, 'Недостаточно товара на складе.')
                    return render(request, 'orders/cart_add.html', {'form': form, 'product': product})
                cart_item.save()
            messages.success(request, f'{product.name} добавлен в корзину.')
            return redirect('orders:cart_detail')
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = CartItemForm()
    return render(request, 'orders/cart_add.html', {'form': form, 'product': product})

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = [
        {
            'product': item.product,
            'quantity': item.quantity,
            'total': item.product.price * item.quantity
        }
        for item in cart.items.all()
    ]
    total_price = sum(item['total'] for item in items)
    return render(request, 'orders/cart.html', {'cart': cart, 'items': items, 'total_price': total_price})

@login_required
def cart_clear(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    messages.success(request, 'Корзина очищена.')
    return redirect('orders:cart_detail')

@login_required
def order_create(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.error(request, 'Корзина пуста.')
        return redirect('products:product_list')
    if request.method == 'POST':
        order = Order.objects.create(user=request.user)
        for item in cart.items.all():
            if item.quantity > item.product.stock:
                order.delete()
                messages.error(request, f'Недостаточно товара {item.product.name} на складе.')
                return redirect('orders:cart_detail')
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            item.product.stock -= item.quantity
            item.product.save()
        cart.items.all().delete()
        messages.success(request, 'Заказ успешно оформлен.')
        return redirect('users:profile')
    return render(request, 'orders/order_form.html', {'cart': cart})

@login_required
def order_list(request):
    orders = request.user.orders.all().prefetch_related('items__product__shop')
    return render(request, 'orders/order_list.html', {'orders': orders})

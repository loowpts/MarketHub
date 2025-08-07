from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import inlineformset_factory
from .models import Product, ProductImage
from .forms import ProductForm
from shops.models import Shop
from users.models import User

ProductImageFormSet = inlineformset_factory(Product, ProductImage, fields=('image',), extra=1, can_delete=True)

def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(shop__status='approved').order_by('-created_at')
    if query:
        products = products.filter(name__icontains=query)
    return render(request, 'products/product_list.html', {
        'products': products,
        'query': query
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.shop.status != 'approved':
        messages.info(request, 'Этот товар принадлежит магазину, который находится на модерации.')
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def product_create(request):
    if request.user.profile.role != 'seller':
        messages.error(request, 'Только продавцы могут добавлять товары.')
        return redirect('users:index')
    user_shops = request.user.shops.filter(status='approved')
    if not user_shops.exists():
        messages.error(request, 'У вас нет одобренного магазина. Создайте или дождитесь одобрения.')
        return redirect('shops:shop_create')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=Product())
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.shop = user_shops.first()
            product.save()
            formset.instance = product
            formset.save()
            messages.success(request, 'Товар успешно создан.')
            return redirect('products:product_detail', pk=product.pk)
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = ProductForm()
        formset = ProductImageFormSet(instance=Product())
    return render(request, 'products/product_form.html', {'form': form, 'formset': formset})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Product, Order, Supplier, User
from .forms import LoginForm, ProductForm, OrderForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('product_list')
    return render(request, 'catalog/login.html', {'form': form})


def guest_login_view(request):
    guest, created = User.objects.get_or_create(
        username='guest',
        defaults={'full_name': 'Гость', 'is_active': True}
    )
    if created:
        guest.set_unusable_password()
        guest.save()
    login(request, guest, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('product_list')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def product_list(request):
    products = Product.objects.select_related('category', 'manufacturer', 'supplier').all()
    suppliers = Supplier.objects.all()

    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(article__icontains=query) | Q(description__icontains=query)
        )

    supplier_id = request.GET.get('supplier', '')
    if supplier_id:
        products = products.filter(supplier_id=supplier_id)

    sort = request.GET.get('sort', '')
    if sort == 'stock_asc':
        products = products.order_by('stock')
    elif sort == 'stock_desc':
        products = products.order_by('-stock')
    else:
        products = products.order_by('name')

    return render(request, 'catalog/product_list.html', {
        'products': products,
        'suppliers': suppliers,
        'query': query,
        'selected_supplier': supplier_id,
        'sort': sort,
    })


@login_required
def product_add(request):
    if not request.user.can_edit_products():
        messages.error(request, 'Недостаточно прав.')
        return redirect('product_list')
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Товар добавлен.')
        return redirect('product_list')
    return render(request, 'catalog/product_form.html', {
        'form': form, 'title': 'Добавить товар', 'is_edit': False
    })


@login_required
def product_edit(request, pk):
    if not request.user.can_edit_products():
        messages.error(request, 'Недостаточно прав.')
        return redirect('product_list')
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Товар «{product.name}» сохранён.')
        return redirect('product_list')
    form.fields['article'].widget.attrs['readonly'] = True
    return render(request, 'catalog/product_form.html', {
        'form': form, 'title': f'Редактировать: {product.name}',
        'product': product, 'is_edit': True
    })


@login_required
def product_delete(request, pk):
    if not request.user.can_edit_products():
        messages.error(request, 'Недостаточно прав.')
        return redirect('product_list')
    product = get_object_or_404(Product, pk=pk)
    if Order.objects.filter(article=product.article).exists():
        messages.error(request, f'Нельзя удалить «{product.name}» — есть связанные заказы.')
        return redirect('product_list')
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Товар «{name}» удалён.')
        return redirect('product_list')
    return render(request, 'catalog/product_confirm_delete.html', {'product': product})


@login_required
def order_list(request):
    if not request.user.can_view_orders():
        messages.error(request, 'Недостаточно прав.')
        return redirect('product_list')
    orders = Order.objects.select_related('delivery_point', 'client').all()
    query = request.GET.get('q', '').strip()
    if query:
        orders = orders.filter(
            Q(client_name__icontains=query) | Q(article__icontains=query)
        )
    return render(request, 'catalog/order_list.html', {'orders': orders, 'query': query})


@login_required
def order_edit(request, pk):
    if not request.user.can_edit_orders():
        messages.error(request, 'Недостаточно прав.')
        return redirect('order_list')
    order = get_object_or_404(Order, pk=pk)
    form = OrderForm(request.POST or None, instance=order)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Заказ №{order.number} обновлён.')
        return redirect('order_list')
    form.fields['number'].widget.attrs['readonly'] = True
    return render(request, 'catalog/order_form.html', {
        'form': form, 'order': order, 'title': f'Заказ №{order.number}'
    })


@login_required
def order_delete(request, pk):
    if not request.user.can_edit_orders():
        messages.error(request, 'Недостаточно прав.')
        return redirect('order_list')
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        num = order.number
        order.delete()
        messages.success(request, f'Заказ №{num} удалён.')
        return redirect('order_list')
    return render(request, 'catalog/order_confirm_delete.html', {'order': order})

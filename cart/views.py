from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from menu.models import Product
from cart.cart import Cart
from cart.forms import CartAddProductForm, CartAddListProductForm
from main.models import Home


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product, cd['quantity'], cd['update'])
    return redirect('cart:detail')


@require_POST
def cart_add_list(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddListProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product, 1, cd['update'])
    return redirect('menu:list')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:detail')


def cart_detail(request):
    config = Home.objects.get(id=1)
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'update': True
        })
    return render(request, 'cart/detail.html', {
        'config': config,
        'cart': cart
    })

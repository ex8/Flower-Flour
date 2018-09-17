from django.shortcuts import render, get_object_or_404
from menu.models import Category, Product
from cart.forms import CartAddListProductForm, CartAddProductForm
from django.contrib import messages
from menu.models import Menu


def menu_list(request, category_slug=None):
    menu = Menu.objects.get(id=1)
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).order_by('sort')
    cart_product_form = CartAddListProductForm()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(available=True, category=category).order_by('sort')
    if cart_product_form.is_valid():
        return messages.success(request=request, message='Successfully added item.')
    return render(request=request, template_name='menu/list.html', context={
        'menu': menu,
        'category': category,
        'categories': categories,
        'products': products,
        'category_slug': category_slug,
        'cart_product_form': cart_product_form
    })


def menu_detail(request, id, slug):
    menu = Menu.objects.get(id=1)
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, template_name='menu/detail.html', context={
        'menu': menu,
        'product': product,
        'cart_product_form': cart_product_form
    })

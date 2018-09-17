from django.shortcuts import render
from orders.models import Order, OrderItem, OrderConfig
from orders.forms import OrderForm, CloverPayForm, CustomCakeOrderForm
from cart.cart import Cart
from cloverapi.cloverapi_client import CloverApiClient
from django.conf import settings
from clover.pay import CloverPay
from base64 import b64encode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from clover.models import Clover
from menu.models import Product
from clover.notification import NotifyService
import requests
from custom_cakes.models import CustomCakeOrderConfigOption


def notify(request):
    return render(request, 'orders/order/notify.html', {

    })


def order_list(request):
    config = OrderConfig.objects.get(id=1)
    return render(request, 'orders/order/list.html', {
        'config': config
    })


def order_delivery(request):
    config = OrderConfig.objects.get(id=1)
    return render(request, 'orders/order/delivery.html', {
        'config': config
    })


def order_custom(request):
    config = OrderConfig.objects.get(id=1)
    options = CustomCakeOrderConfigOption.objects.filter(available=True).order_by('sort')
    if request.method == 'POST':
        custom_cake_order_form = CustomCakeOrderForm(data=request.POST,options=options)
        order_form = OrderForm(request.POST)
        if custom_cake_order_form.is_valid() and order_form.is_valid():
            product = Product.objects.get(slug='custom-cake')
            new_order = order_form.save()
            OrderItem(price=product.price, quantity=1, product=product, order_id=new_order.id).save()
            new_order.send_admin_custom_cake_confirm_emails(custom_cake_order_form.cleaned_data)
            new_order.send_client_custom_cake_confirm_emails(custom_cake_order_form.cleaned_data)
            return render(request, template_name='orders/order/custom-done.html', context={
                'config': config
            })
    else:
        custom_cake_order_form = CustomCakeOrderForm(options)
        # cake_form = CustomCakeForm()
        order_form = OrderForm()
    return render(request, 'orders/order/custom.html', {
        'config': config,
        # 'cake_form': cake_form,
        'order_form': order_form,
        'ok': custom_cake_order_form
    })


def order_create(request):
    config = OrderConfig.objects.get(id=1)
    access_token = Clover.objects.filter().latest('achieved').access_token
    clover = CloverApiClient(api_url=settings.CLOVER_API_URL,
                             merchant_id=settings.CLOVER_MERCHANT_ID,
                             api_key=access_token)
    cart = Cart(request)
    order_items_m = []
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        card_form = CloverPayForm(request.POST)
        if order_form.is_valid() and card_form.is_valid():
            order = order_form.save()
            # Create OrderItems for FF internal DB
            for item in cart:
                order_item = OrderItem(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                order_item.save()
                order_items_m.append(order_item.product.name)

            # Send to Clover PoS, total is converted to cents
            clover_order = clover.order_service.create_order({
                'state': 'open',
                'title': str(order.id),
                'total': (float(order.get_total_cost()) * 100),
                'currency': 'USD',
            })
            # Create Clover LineItem(s)
            for item in cart:
                if item['quantity'] > 1:
                    for el in range(item['quantity']):
                        clover.order_service.create_line_item(
                            order_id=clover_order['id'],
                            line_item={
                                'name': str(item['product']),
                                'price': float(item['price'] * 100),
                            }
                        )
                else:
                    clover.order_service.create_line_item(
                        order_id=clover_order['id'],
                        line_item={
                            'name': str(item['product']),
                            'price': float(item['price'] * 100),
                        }
                    )

            # Clover CC Pay
            clover_pay = CloverPay(api_url=settings.CLOVER_API_URL,
                                   merchant_id=settings.CLOVER_MERCHANT_ID,
                                   api_key=access_token)
            card = card_form.cleaned_data
            secrets = clover_pay.get_secrets()
            card_number = card['card_number'].encode()
            # card_number = b'4242424242424242'
            modulus = int(secrets['modulus'])
            exponent = int(secrets['exponent'])
            prefix = secrets['prefix'].encode()
            RSAkey = RSA.construct((modulus, exponent))
            cipher = PKCS1_OAEP.new(RSAkey)
            encrypted = cipher.encrypt(prefix + card_number)
            card_encrypted = b64encode(encrypted).decode()
            payload = {
                "orderId": clover_order['id'],
                "zip": card['zip_code'],
                "expMonth": card['exp_month'],
                "cvv": card['cvv'],
                "amount": (float(order.get_total_cost()) * 100),
                "currency": "usd",
                "last4": card['card_number'][-4:],
                "expYear": card['exp_year'],
                "first6": card['card_number'][0:6],
                "cardEncrypted": card_encrypted
            }
            payment = clover_pay.send_payment(payload)
            if payment['result'] == 'APPROVED':
                order.paid = True
                order.save()
                order.send_client_order_confirm_email(order_items_m, clover_order, payment)
                order.send_admin_order_confirm_emails(order_items_m, clover_order, payment)
                order.send_admin_order_confirm_sms(clover_order)
                cart.clear()
                return render(request, 'orders/order/created.html', {
                    'config': config
                })
            else:
                return render(request, 'orders/order/pay-error.html', {
                    'config': config
                })
        else:
            return render(request, 'orders/order/order-error.html', {
                'config': config
            })
    else:
        order_form = OrderForm()
        card_form = CloverPayForm()
    return render(request, 'orders/order/create.html', {
        'config': config,
        'order_form': order_form,
        'card_form': card_form,
        'cart': cart,
    })

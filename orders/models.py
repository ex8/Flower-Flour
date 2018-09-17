from django.db import models
from menu.models import Product
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from twilio.rest import Client
from django.conf import settings


class OrderConfig(models.Model):
    list_banner_image = models.ImageField(upload_to='orders')
    delivery_banner_image = models.ImageField(upload_to='orders')
    custom_banner_image = models.ImageField(upload_to='orders')
    create_banner_image = models.ImageField(upload_to='orders')


class Order(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=25)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '#{}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.order_items.all())

    def send_admin_order_confirm_sms(self, clover):
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            client = Client(settings.TWILIO_ACCOUNT, settings.TWILIO_TOKEN)
            client.messages.create(
                to=admin.profile.phone,
                from_=settings.TWILIO_NUMBER,
                body='NEW order from website! Clover Order ID #{}'.format(clover['id'])
            )

    def send_client_custom_cake_confirm_emails(self, cake):
        mail = EmailMessage(to=[
            {
                'address': self.email,
                'substitution_data': {
                    'first_name': self.first_name,
                    'name': '{} {}'.format(self.first_name, self.last_name),
                    'phone': self.phone,
                    'created': self.created.strftime('%m/%d/%y'),
                    'cake': str(cake)
                }
            }
        ], from_email='noreply@flower-flour.com')
        mail.template = 'client-custom-cake-confirm'
        mail.send()

    def send_admin_custom_cake_confirm_emails(self, cake):
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            mail = EmailMessage(to=[
                {
                    'address': admin.email,
                    'substitution_data': {
                        'first_name': admin.first_name,
                        'name': '{} {}'.format(self.first_name, self.last_name),
                        'phone': self.phone,
                        'created': self.created.strftime('%m/%d/%y'),
                        'cake': str(cake)
                    }
                }
            ], from_email='noreply@flower-flour.com')
            mail.template = 'admin-custom-cake-confirm'
            mail.send()

    def send_client_order_confirm_email(self, order_items, clover_order, clover_payment):
        mail = EmailMessage(to=[
            {
                'address': self.email,
                'substitution_data': {
                    'first_name': self.first_name,
                    'order_id': clover_order['id'],
                    'currency': clover_order['currency'],
                    'created': self.created.strftime('%m/%d/%y'),
                    'payment_id': clover_payment['paymentId'],
                    'mail_address': self.address,
                    'postal': self.postal_code,
                    'city': self.city,
                    'order_items': str(order_items)
                }
            }
        ], from_email='noreply@flower-flour.com')
        mail.template = 'order-confirm'
        mail.send()

    def send_admin_order_confirm_emails(self, order_items, clover_order, clover_payment):
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            mail = EmailMessage(to=[
                {
                    'address': admin.email,
                    'substitution_data': {
                        'first_name': admin.first_name,
                        'client_first': self.first_name,
                        'client_last': self.last_name,
                        'client_email': self.email,
                        'client_address': self.address,
                        'client_postal': self.postal_code,
                        'client_city': self.city,
                        'client_phone': self.phone,
                        'order_created': self.created.strftime('%m/%d/%y'),
                        'clover_order_id': clover_order['id'],
                        'clover_pay_id': clover_payment['paymentId'],
                        'order_items': str(order_items)
                    }
                }
            ], from_email='noreply@flower-flour.com',
                subject='New Order {} Confirmation | Flower Flour'.format(clover_order['id']))
            mail.template = 'admin-order-confirm'
            mail.send()


class OrderItem(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, related_name='items')
    order = models.ForeignKey(Order, related_name='order_items')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.quantity * self.price

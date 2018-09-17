from django.db import models
from custom_cakes import config
from orders.models import Order
from multiselectfield import MultiSelectField

CHOICES = (
    ('cake', 'Cake'),
    ('bread', 'Bread'),
    ('chocolate', 'Chocolate'),
    ('butter', 'Butter'),
    ('sweet', 'Sweet')
)


class CustomCakeConfig(models.Model):
    banner_image = models.ImageField(upload_to='custom-cakes')


class Cake(models.Model):
    image = models.ImageField(upload_to='cakes')
    name = models.CharField(max_length=50)
    small_description = models.CharField(max_length=50)
    big_description = models.TextField(max_length=250)
    available = models.BooleanField(default=True)
    mixitup = MultiSelectField(choices=CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CustomCakeOrder(models.Model):
    date_needed = models.DateTimeField()
    type = models.CharField(choices=config.CAKE_TYPES, max_length=50)
    size = models.CharField(choices=config.CAKE_SIZES, max_length=50)
    servings = models.PositiveIntegerField()
    tiers = models.PositiveIntegerField()
    flavor = models.CharField(choices=config.CAKE_FLAVORS, max_length=10)
    filling1 = models.CharField(choices=config.CAKE_FILLING1, max_length=50)
    filling2 = models.CharField(choices=config.CAKE_FILLING2, max_length=50, blank=True)
    filling3 = models.CharField(choices=config.CAKE_FILLING3, max_length=50, blank=True)
    frosting_color = models.CharField(max_length=50)
    decoration_colors = models.CharField(max_length=100, blank=True)
    writing = models.CharField(max_length=100, blank=True)
    picture = models.ImageField(upload_to='custom-cakes', blank=True)
    message = models.TextField()
    complete = models.BooleanField(default=False)
    order = models.ForeignKey(Order, related_name='customcake')

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return 'Custom Cake #{} for Order #{}'.format(self.id, self.order.id)


class CustomCakeOrderConfigOption(models.Model):
    FORM_CHOICES = (
        ('date', 'Date'),
        ('dropdown', 'Dropdown'),
        ('input', 'Input'),
    )
    name = models.CharField(max_length=50)
    form_type = models.CharField(max_length=50, choices=FORM_CHOICES)
    sort = models.PositiveIntegerField(default=9999)
    available = models.BooleanField(default=False)

    class Meta:
        ordering = ('sort',)

    def __str__(self):
        return self.name


class CustomCakeOrderConfigOptionItem(models.Model):
    name = models.CharField(max_length=50)
    sort = models.PositiveIntegerField(default=9999)
    config_option = models.ForeignKey(CustomCakeOrderConfigOption, related_name='config_option_item')

    class Meta:
        ordering = ('sort',)

    def __str__(self):
        return self.name

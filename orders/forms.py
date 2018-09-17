from django import forms
from orders.models import Order
from custom_cakes import config
from custom_cakes.models import CustomCakeOrder, CustomCakeOrderConfigOptionItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city', 'phone']
        widgets = {
            'phone': forms.TextInput(attrs={
                'placeholder': 'ex. (111) 222-3456'
            })
        }


class CloverPayForm(forms.Form):
    card_number = forms.CharField(required=True, widget=forms.TextInput)
    exp_month = forms.CharField(required=True, widget=forms.TextInput)
    exp_year = forms.CharField(required=True, widget=forms.TextInput)
    cvv = forms.CharField(required=True, widget=forms.TextInput)
    zip_code = forms.CharField(required=True, widget=forms.TextInput)


# For HTML5 DateTimer JS Picker (override widget)
class DateTimeInput(forms.DateTimeInput):
    input_type = 'date'


class CustomCakeOrderForm(forms.Form):
    def __init__(self, options, *args, **kwargs):
        super(CustomCakeOrderForm, self).__init__(*args, **kwargs)
        for option in options:
            if option.form_type == 'date':
                self.fields[option.name] = forms.DateTimeField(widget=DateTimeInput)
            elif option.form_type == 'dropdown':
                items = CustomCakeOrderConfigOptionItem.objects.filter(config_option=option).order_by('sort')
                choices = [(i, i) for i in items]
                self.fields[option.name] = forms.ChoiceField(choices=choices)
            elif option.form_type == 'input':
                self.fields[option.name] = forms.CharField()


# class CustomCakeForm(forms.ModelForm):
#     class Meta:
#         model = CustomCakeOrder
#         fields = ('date_needed', 'type', 'size', 'servings', 'tiers',
#                   'flavor', 'filling1', 'filling2', 'filling3', 'frosting_color',
#                   'decoration_colors', 'writing', 'picture', 'message')
#         widgets = {
#             'date_needed': forms.DateTimeInput(attrs={
#                 'placeholder': "Date Needed (YYYY-MM-DD)",
#                 'type': 'date'
#             }),
#             'type': forms.Select(choices=config.CAKE_TYPES),
#             'size': forms.Select(choices=config.CAKE_SIZES),
#             'servings': forms.TextInput(attrs={
#                 'placeholder': "Number of serving(s)"
#             }),
#             'tiers': forms.TextInput(attrs={
#                 'placeholder': "Number of cake tier(s)"
#             }),
#             'flavor': forms.Select(choices=config.CAKE_FLAVORS),
#             'filling1': forms.Select(choices=config.CAKE_FILLING1),
#             'filling2': forms.Select(choices=config.CAKE_FILLING2),
#             'filling3': forms.Select(choices=config.CAKE_FILLING3),
#             'frosting_color': forms.TextInput(attrs={
#                 'placeholder': "Frosting color ex. [red, blue, green]"
#             }),
#             'decoration_colors': forms.TextInput(attrs={
#                 'placeholder': "Decoration color(s) ex. [red, orange, pink]"
#             }),
#             'writing': forms.TextInput(attrs={
#                 'placeholder': "Custom, written message on the cake"
#             }),
#             'message': forms.TextInput(attrs={
#                 'placeholder': "Describe the cake in detail to help our chefs!"
#             })
#         }

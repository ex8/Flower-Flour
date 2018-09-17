from django import template

register = template.Library()

@register.filter
def to_list(value):
    return str(value).replace(',', '')

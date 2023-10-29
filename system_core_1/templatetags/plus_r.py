from django import template

register = template.Library()

@register.filter(name='plus_r')
def plus_r(value):
    return value.split('+')[0]

@register.filter(name='rom')
def rom(value):
    return value.split('+')[1]

@register.filter(name='format_price')
def format_price(value):
    value = str(value).split('.')[0]
    value = int(value)
    return f"MK{value:,}"
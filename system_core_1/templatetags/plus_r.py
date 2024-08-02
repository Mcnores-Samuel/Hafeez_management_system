from django import template


register = template.Library()


@register.filter(name='plus_r')
def plus_r(value):
    if value:
        return value.split('+')[0]
    return value


@register.filter(name='rom')
def rom(value):
    if value:
        return value.split('+')[1]
    return value


@register.filter(name='format_price')
def format_price(value):
    if value:
        value = str(value).split('.')[0]
        value = int(value)
        return f"{value:,}"
    return f"{value:,}"


@register.filter(name='username_format')
def username_format(value):
    if '-' in value:
        value = value.split('-')
        value = f"{value[0]} ({value[1]})"
    elif '_' in value:
        value = value.split('_')
        value = f"{value[0]} ({str(value[1]).capitalize()})"
    return value
    

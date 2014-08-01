from django import template

register = template.Library()

@register.filter(name='access')
def access(value, arg):
    try:
        return value[arg]
    except KeyError:
        return ''

@register.filter(name='get_type_list')
def get_type_list(list):
    if list:
        return list[0].__class__.__name__
    return ""
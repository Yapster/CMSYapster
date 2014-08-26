from django import template
import boto

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

@register.filter(name='get_url_yapsterapp_s3')
def get_url_yapsterapp_s3(path):
    if path:
        c = boto.connect_s3()
        b = c.get_bucket('yapsterapp')
        if b:
            try:
                return b.get_key(path).generate_url(expires_in=600)
            except:
                return ""
        return ""
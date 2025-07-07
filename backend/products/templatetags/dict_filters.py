# yourapp/templatetags/dict_filters.py
from django import template

register = template.Library()

@register.filter(name='dict_get')
def dict_get(d, key):
    return d.get(key, [])

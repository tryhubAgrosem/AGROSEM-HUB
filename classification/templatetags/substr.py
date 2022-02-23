import re
from django import template

register = template.Library()

def substr(value, arg):
    if arg in str(value):
        return arg
    else:
        return ''

register.filter('substr', substr)
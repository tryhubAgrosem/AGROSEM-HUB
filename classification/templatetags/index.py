import re
from django import template

register = template.Library()

def index(value, index):
    return value[index]

register.filter('index', index)
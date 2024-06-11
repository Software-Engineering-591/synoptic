from django import template
from datetime import datetime

register = template.Library()


@register.filter(name='unix_to_datetime')
def unix_to_datetime(value):
    return datetime.fromtimestamp(int(value))

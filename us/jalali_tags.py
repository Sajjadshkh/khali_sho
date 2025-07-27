from django import template
from jalali_date import datetime2jalali

register = template.Library()

@register.filter
def to_jalali(value, fmt="%Y/%m/%d"):
    if not value:
        return ''
    return datetime2jalali(value).strftime(fmt)
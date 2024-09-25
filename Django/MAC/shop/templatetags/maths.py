from django import template
register = template.Library()

@register.filter
def add(val1,val2):
    value = val1+val2
    return value

@register.filter
def multiply(val1,val2):
    value = val1*val2
    return value

@register.filter
def divide(val1,val2):
    value = val1/val2
    return value

@register.filter
def subtract(val1,val2):
    value = val1-val2
    return value


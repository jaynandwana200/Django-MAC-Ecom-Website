from django import template
register = template.Library()


@register.filter
def add4(value):
    value = value+4
    return value


@register.filter
def discountedprice(price,discount):
    return price-price*(discount/100) 


@register.filter
def subtract(num1,num2):
    return num1 - num2

@register.filter
def pop(num):
    num.pop()
    return "  "

@register.filter
def list_item(lst, i):
    try:
        return lst[i]
    except:
        return None
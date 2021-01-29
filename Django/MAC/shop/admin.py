from django.contrib import admin
from .models import orderdetails, product, customer ,contact, shippingaddress
from rangefilter.filter import DateRangeFilter
from admin_numeric_filter.admin import RangeNumericFilter

# Register your models here.


class AdminProduct(admin.ModelAdmin):
    list_display = ['product_name', 'category', 'stock', 'price']
    list_filter = (("stock", RangeNumericFilter), "brand", "category", "subcategory", ("pub_date",
    DateRangeFilter), ("price", RangeNumericFilter), ("discount", RangeNumericFilter))
    search_fields = ['product_name']


class Admincustomer(admin.ModelAdmin):
    list_display = ['customer_id', 'customer_name', 'Email_id', 'phone_no']
    search_fields = ['customer_name','customer_id','Email_id']
    
class Admincontact(admin.ModelAdmin):
    list_display = ['mail', 'name', 'phone','country']
    search_fields = ['mail','country','name']

class Adminorderdetails(admin.ModelAdmin):
    list_display = ['order_id', 'name_on_card', 'credit_card_number']
    search_fields = ['order_id','name_on_card','credit_card_number']

class Adminshippingaddress(admin.ModelAdmin):
    list_display = ['order_id', 'fullname', 'mail_id','zip']
    search_fields = ['order_id','fullname','zip','city','state','country']

admin.site.register(product, AdminProduct)
admin.site.register(customer, Admincustomer)
admin.site.register(contact,Admincontact)
admin.site.register(orderdetails,Adminorderdetails)
admin.site.register(shippingaddress,Adminshippingaddress)


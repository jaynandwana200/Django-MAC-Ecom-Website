from . import views
from django.urls import path
from django.contrib import admin

admin.site.site_header = "MAC Administration"
admin.site.site_title = "MAC Admin"
admin.site.index_title = "Welcome to MAC Administration"

urlpatterns = [
    path("", views.index, name="shophome"),
    path("about/", views.about, name="aboutus"),
    path("contactus/", views.contactus, name="contactus"),
    path("myorders/", views.myorders, name="myorders"),
    path("productview/", views.productview, name="productview"),
    path("checkout/", views.checkout, name="checkout"),
    path("categories/", views.categories, name="categories"),
    path("signin/", views.signin, name="signin"),
    path("createcustomer/", views.createcustomer, name="createcustomer"),
    path("mycart/", views.mycart, name="mycart"),
    path("sale/", views.sale, name="sale"),
    path("handelrequest/",views.handelrequest,name="handelrequest")
]

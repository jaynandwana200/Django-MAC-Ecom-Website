from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, EmailField
from django.db.models.fields.related import ForeignKey
# Create your models here.


class product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50, default="", blank=True)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="", blank=True)
    image = models.ImageField(upload_to="shop/images", default="")
    desc = models.CharField(max_length=300, blank=True)
    pub_date = models.DateField()
    price = models.IntegerField(default=0)
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    discount = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)], default=0)

    def __str__(self):
        return self.product_name


class customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100, blank=False)
    Email_id = models.EmailField(max_length=100, blank=False)
    phone_no = models.CharField(blank=False, max_length=15)
    password = models.CharField(max_length=500)

    def __int__(self):
        return self.user_id

    def register(self):
        self.save()


    def phonenumber(value):
        if(len(value) > 10):
            return "error"
        elif(len(value) < 10):
            return "error"
        return "ok"

    def passwordvalidator(value):
        if(len(value) < 9):
            return "error"
        else:
            return "ok"


class contact(models.Model):

    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default="")
    mail = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)

    def __str__(self):
        return self.mail
    
    def register(self):
        self.save()


class orderdetails(models.Model):
    order_id = models.AutoField(primary_key=True)
    session_id = models.CharField(max_length=100,default="")
    item_json = models.CharField(max_length=10000,default="") 
    name_on_card = models.CharField(max_length=100)
    credit_card_number = models.CharField(max_length=50)
    Exp_month = models.CharField(max_length=50)
    cvv =models.CharField(max_length=10)
    Exp_year=models.CharField(max_length=10)
    amount = models.CharField(max_length=100,default="")

    def __int__(self):
        return self.order_id

    def register(self):
        self.save()


class shippingaddress(models.Model):
    order_id = models.ForeignKey(orderdetails,on_delete=CASCADE)
    fullname = models.CharField(max_length=100)
    mail_id = models.EmailField(max_length=100)
    Address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=50)
    
    def __int__(self):
        return self.order_id

    def register(self):
        self.save()

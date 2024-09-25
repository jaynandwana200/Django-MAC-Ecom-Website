from django.db import connection
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import orderdetails, product
from .models import customer,contact,shippingaddress
from django.contrib.auth.hashers import make_password,check_password 
from math import ceil
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from paytm import checksum
from django.contrib.auth import login,logout,authenticate
MERCHANT_KEY='Ee6zeIgR@SNQKu_Z'
# Create your views here.

def index(request):
    ############################## Raw SQL ############################
    products = product.objects.raw('SELECT * FROM shop_product')
    catemp = product.objects.raw('select category,id from shop_product')
    ###########################  Product category logic  #######################
    categories = set()
    for items in catemp:
        categories.add(items.category)
    categ = []
    for idx, item in enumerate(categories):
        categ.append({item: []})
        for ele in products:
            if(list(categ[idx].keys())[0] == ele.category):
                categ[idx][list(categ[idx].keys())[0]].append(ele)
    i = 0
    j = 0
    first5 = []
    categor = []
    for items in categories:
        categor.append(items)
    for items in categories:
        first5.append([])
    for item in categ:
        for item1 in item:
            i = 0
            while(i < 5):
                if(i == len(item.get(item1))):
                    break
                first5[j].append(item.get(item1)[i])
                i = i+1
            j = j+1
    nslides1 = []
    biglist = []
    for item in categ:
        nslides1.append(0)
        biglist.append(0)
    q = 0
    ########################### slider logic ##################################
    for items in categ:
        imp = items[categories.pop()]
        n = len(imp)
        nslides = n//5 + ceil(n/5-(n//5))
        nslides1[q] = nslides
        i = 5
        j = 0
        biglist[q] = list(range(nslides1[q]-1))
        for k in biglist[q]:
            biglist[q][k] = {}
        while(i < n):
            biglist[q][j][i] = imp[i]
            i = i+1
            if((i) % 5 == 0):
                j = j+1
        q = q+1
    allproducts = []
    z = 0
    for i in categ:
        allproducts.append({'product': i, 'list': biglist[z], 'range': range(
            1, nslides1[z]), 'no_of_slides': nslides1[z], 'first5': first5[z]})
        z = z+1
    ########################################### #########################################
    customers=request.session.get("customer")
    custom=serializers.deserialize("json", customers) ## deserializing json 
    name=""
    if customers != None:
        for items in custom:
            name=items.object.customer_name
    ###################################################################################
    params = {'allproducts': allproducts, 'categories': categor,"currentuser":name}
    return render(request, 'shop/index.html', params)


def about(request):
    customers=request.session.get("customer")
    custom=serializers.deserialize("json", customers) ## deserializing json 
    name=""

    products = product.objects.raw('SELECT * FROM shop_product')
    catemp = product.objects.raw('select category,id from shop_product')
    categories = set()
    for items in catemp:
        categories.add(items.category)
    categ = []
    for idx, item in enumerate(categories):
        categ.append({item: []})
        for ele in products:
            if(list(categ[idx].keys())[0] == ele.category):
                categ[idx][list(categ[idx].keys())[0]].append(ele)
    categor = []
    for items in categories:
        categor.append(items)


    params={}
    params["categories"]=categor
    if customers != None:
        for items in custom:
            name=items.object.customer_name
    params["currentuser"]=name
    return render(request, 'shop/about.html',params)


def contactus(request):

    products = product.objects.raw('SELECT * FROM shop_product')
    catemp = product.objects.raw('select category,id from shop_product')
    categories = set()
    for items in catemp:
        categories.add(items.category)
    categ = []
    for idx, item in enumerate(categories):
        categ.append({item: []})
        for ele in products:
            if(list(categ[idx].keys())[0] == ele.category):
                categ[idx][list(categ[idx].keys())[0]].append(ele)
    categor = []
    for items in categories:
        categor.append(items)

    if(request.method=="GET"):
        customers=request.session.get("customer")
        custom=serializers.deserialize("json", customers) ## deserializing json 
        name=""
        params={}
        params["categories"]=categor
    if customers != None:
        for items in custom:
            name=items.object.customer_name
        params["currentuser"]=name
        return render(request, 'shop/contactus.html',params)
    else:
        customname = request.POST.get("name","")
        mail_id = request.POST.get("emailid","")
        number = request.POST.get("phone","")
        county = request.POST.get("country","")
        desc = request.POST.get("subject","")
        if(customname=="" or mail_id=="" or number=="" or county=="" or desc==""):
            params = {"alert":"filldetails"}
            return render(request,'shop/contactus.html',params)
        Contact = contact(name=customname,mail=mail_id,phone=number,country=county,desc=desc)
        Contact.register()
        return redirect('shophome')


def myorders(request):

    products = product.objects.raw('SELECT * FROM shop_product')
    catemp = product.objects.raw('select category,id from shop_product')
    categories = set()
    for items in catemp:
        categories.add(items.category)
    categ = []
    for idx, item in enumerate(categories):
        categ.append({item: []})
        for ele in products:
            if(list(categ[idx].keys())[0] == ele.category):
                categ[idx][list(categ[idx].keys())[0]].append(ele)
    categor = []
    for items in categories:
        categor.append(items)


    customers=request.session.get("customer")
    custom=serializers.deserialize("json", customers) ## deserializing json 
    name=""
    params={}
    if customers != None:
        for items in custom:
            name=items.object.customer_name
    params["currentuser"]=name
    if name == "" : return render(request,'shop/myorders.html',params)
    ###########################raw sql queries###########################
    order_details = orderdetails.objects.raw('select * from shop_orderdetails')
    customers=request.session.get("customer")
    custom=serializers.deserialize("json", customers) ## deserializing json 
    orders=[]
    product_ids=[]
    mail = ""
    if customers != None:    
        for item in custom:
            mail=str(item.object.Email_id)
    product_gr=[]
    ids=[]
    for items in order_details:
        if(items.Email_id==mail):
            orders.append(items)
            ids.append(items.order_id)
            product_ids.append(items.item_json)
    i=0
    resultant = []
    for item in order_details:
        if(item.Email_id==mail):
            product_gr.append(json.loads(item.item_json))
            resultant.append([])
    ###############################################################
    i=0
    for items in product_gr:
        for item in items:
            resultant[i].append(items.get(item))
        i=i+1
    params["orders"]=resultant
    ids.reverse()
    params["ids"]=ids
    params["categories"]=categor
    return render(request, 'shop/myorders.html',params)


def productview(request):

    products = product.objects.raw('SELECT * FROM shop_product')
    catemp = product.objects.raw('select category,id from shop_product')
    categories = set()
    for items in catemp:
        categories.add(items.category)
    categ = []
    for idx, item in enumerate(categories):
        categ.append({item: []})
        for ele in products:
            if(list(categ[idx].keys())[0] == ele.category):
                categ[idx][list(categ[idx].keys())[0]].append(ele)
    categor = []
    for items in categories:
        categor.append(items)
    

    products = product.objects.raw('SELECT * FROM shop_product')
    ####################################################### 
    ########################################################
    prodview=request.GET.get("products","default")## fetching data from index page
    stoc = 0
    for items in products:
        if(str(items.id) == str(prodview)):
            stoc = items.stock
    params={}
    params["categories"]=categor
    for items in products:
        if(str(items.id)==prodview):
            params["product"]=items
    disprice=params["product"].price - params["product"].price * (params["product"].discount / 100)
    params["disprice"]=disprice
    #######################################################
    customers=request.session.get("customer")
    custom=serializers.deserialize("json", customers) ## deserializing json 
    name=""
    if customers != None:
        for items in custom:
            name=items.object.customer_name
    params["currentuser"]=name
    params["stock"]=stoc
    return render(request,'shop/productview.html',params)


def signin(request):

    products = product.objects.raw('SELECT * FROM shop_product')
    catemp = product.objects.raw('select category,id from shop_product')
    categories = set()
    for items in catemp:
        categories.add(items.category)
    categ = []
    for idx, item in enumerate(categories):
        categ.append({item: []})
        for ele in products:
            if(list(categ[idx].keys())[0] == ele.category):
                categ[idx][list(categ[idx].keys())[0]].append(ele)
    categor = []
    for items in categories:
        categor.append(items)



    customers=request.session.get("customer")
    custom=serializers.deserialize("json", customers) ## deserializing json 
    name=""
    if customers != None:
        for items in custom:
            name=items.object.customer_name
    params = {}
    params["categories"]=categor
    params["currentuser"]=name
    if(request.method=="GET"):
        return render(request, 'shop/signin.html',params)
    else:
        #################### Raw SQL #############################
        custom = customer.objects.raw('select * from shop_customer;')
        ##############################################################
        email=request.POST.get("emailid","") #fetching data from webpage
        passw=request.POST.get("password","")
        for items in custom:
            if(check_password(passw,items.password) and items.Email_id==email):
                customers = serializers.serialize('json', [ items, ])### converting customer object into json serializable
                request.session["customer"]=customers ## creating sessions ##json serializing creates js objects
                return redirect("shophome")## redirecting to home page
        params["alert"]="incorrectcredentials"
        return render(request, 'shop/signin.html',params)


def signout(request):
    try:
        del request.session['customer']
    except:
        return redirect('shophome')
    return redirect('shophome')


def checkout(request):

    products = product.objects.raw('SELECT * FROM shop_product')
    catemp = product.objects.raw('select category,id from shop_product')
    categories = set()
    for items in catemp:
        categories.add(items.category)
    categ = []
    for idx, item in enumerate(categories):
        categ.append({item: []})
        for ele in products:
            if(list(categ[idx].keys())[0] == ele.category):
                categ[idx][list(categ[idx].keys())[0]].append(ele)
    categor = []
    for items in categories:
        categor.append(items)


    if(request.method=="GET"):
        customers=request.session.get("customer")
        custom=serializers.deserialize("json", customers) ## deserializing json 
        name=""
        email = ""
        params={}
        params["categories"]=categor
        if customers != None:
            for items in custom:
                name=items.object.customer_name
        params["currentuser"]=name
        return render(request, 'shop/checkout.html',params)
    else:
     ######################################################
        item_json = request.POST.get("itemjson","")
        names = request.POST.get("name","")
        address = request.POST.get("address","")
        city = request.POST.get("city","")
        state = request.POST.get("state","")
        country = request.POST.get("country","")
        zip = request.POST.get("zip","")
        nameoncard = request.POST.get("cardname","")
        cardno = request.POST.get("cardnumber","")
        expmonth = request.POST.get("expmonth","")
        expyear = request.POST.get("expyear","")
        cvv = request.POST.get("cvv","")
        amount = request.POST.get("amount","")
    #############################stock logic###################################

        dict=json.loads(item_json)
        stock = []
        for items in dict:
            stock.append({items:dict.get(items)[0]})
        for items in stock:
            for item in items:
                stockbuy=items.get(item)
                stockid =item[2:]
                for items in  product.objects.raw('SELECT * FROM shop_product'):
                    if(str(items.id) == str(stockid)):
                        items.stock = items.stock - stockbuy
                        items.save()
    
    ######################################################################
        email = ""
        if(amount=="0"):
            params={"cart":"empty","currentuser":""}
            return render(request,'shop/checkout.html',params)
        ##############################################################
        customers=request.session.get("customer")
        custom=serializers.deserialize("json", customers) ## deserializing json 
        session_id=" "
        if customers != None:
            for items in custom:
                email = items.object.Email_id
                session_id=items.object.customer_id
        ################################################################
        Orderdetails = orderdetails(Email_id = email,name_on_card=nameoncard,credit_card_number=cardno,Exp_month=expmonth,cvv=cvv,Exp_year=expyear,item_json=item_json,session_id=session_id,amount=amount)
        Orderdetails.register()
        Shippingaddress = shippingaddress(fullname=names,mail_id=email,Address=address,city=city,state=state,country=country,zip=zip,order_id_id=Orderdetails.order_id)
        Shippingaddress.register()
        order_ids = Orderdetails.order_id
        params = {"order":order_ids}
        if(request.POST.get("paytm","default")!="PayTm"):
            if(names=="" or email=="" or address=="" or city=="" or state=="" or country=="" or zip=="" or nameoncard =="" or cardno=="" or expmonth =="" or expyear=="" or cvv ==""):
                params = {"alert":"filldetails"}
                return render(request,'shop/checkout.html',params)
            return render(request, 'shop/sucess.html',params)
        ########################################################
        if(names=="" or email=="" or address=="" or city=="" or state=="" or country=="" or zip==""):
                params = {"alert":"filldetails"}
                return render(request,'shop/checkout.html',params)
        # paytm payment integration
        param_dict = {

                'MID': 'dKNaVh82026476278151',
                'ORDER_ID': str(order_ids),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handelrequest/',

        }
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})


def createcustomer(request):

    products = product.objects.raw('SELECT * FROM shop_product')
    catemp = product.objects.raw('select category,id from shop_product')
    categories = set()
    for items in catemp:
        categories.add(items.category)
    categ = []
    for idx, item in enumerate(categories):
        categ.append({item: []})
        for ele in products:
            if(list(categ[idx].keys())[0] == ele.category):
                categ[idx][list(categ[idx].keys())[0]].append(ele)
    categor = []
    for items in categories:
        categor.append(items)

    ######################## Raw SQL ################################
    custom = customer.objects.raw('select * from shop_customer;')
    ################################################################
    customers=request.session.get("customer")
    cust=serializers.deserialize("json", customers) ## deserializing json 
    name=""
    if customers != None:
        for items in cust:
            name=items.object.customer_name
    params = {}
    params["categories"]=categor
    params["currentuser"]=name
    if(request.method=="GET"):
        return render(request, 'shop/createcustomer.html',params)
    else:
        ################    Sign up constraints   #################
        custome=request.POST.get("customername","")
        email=request.POST.get("Emailid","")
        phone=request.POST.get("phoneno","")  #fetching data from web page
        passw=request.POST.get("password","")
        reppassw=request.POST.get("passwordrepeat","")
        numbers=['0','1','2','3','4','5','6','7','8','9']
        punctuations = '''!()[{]};:'"\,<>/?@#$%^&*_~'''
        for items in custome:
            if (items in punctuations):
                params={"alert":"wrongname"}
                return render(request, 'shop/createcustomer.html',params)
        for items in phone:
            if(items not in numbers):
                params={"alert":"wrongnumber"}
                return render(request, 'shop/createcustomer.html',params)               
        for customers in custom:
            if(customers.Email_id==email):
                params={"alert":"emailexist"}
                return render(request, 'shop/createcustomer.html',params) 
        for customers in custom:
            if(customers.phone_no==phone):
                params={"alert":"phoneexist"}
                return render(request, 'shop/createcustomer.html',params) 
        if(custome=="" or email=="" or phone=="" or passw==""):
            params={"alert":"empty"}
            return render(request, 'shop/createcustomer.html',params)
        if(customer.passwordvalidator(passw)=="error"):
            params={"alert":"passerror"}
            return render(request, 'shop/createcustomer.html',params)
        if(passw!=reppassw):
            params={"alert":"passnotmatch"}
            return render(request, 'shop/createcustomer.html',params)
        if(customer.phonenumber(phone)=="error"):
            params={"alert":"phoneerror"}
            return render(request, 'shop/createcustomer.html',params)
        ##################################################################
        Customer=customer(customer_name = custome,Email_id = email,phone_no = phone,password =make_password(passw))#creating customer
        Customer.register()#saving customer
        Custom = customer.objects.raw('select * from shop_customer;')
        for items in Custom:
            if(check_password(passw,items.password) and items.Email_id==email):
                customers = serializers.serialize('json', [ items, ])### converting customer object into json serializable
                request.session["customer"]=customers ## creating sessions ##json serializing creates js objects
                return redirect("shophome")## redirecting to home page
        return redirect('shophome')


def categories(request):

    products = product.objects.raw('SELECT * FROM shop_product')
    catemp = product.objects.raw('select category,id from shop_product')
    categories = set()
    for items in catemp:
        categories.add(items.category)
    categ = []
    for idx, item in enumerate(categories):
        categ.append({item: []})
        for ele in products:
            if(list(categ[idx].keys())[0] == ele.category):
                categ[idx][list(categ[idx].keys())[0]].append(ele)
    categor = []
    for items in categories:
        categor.append(items)


    ####################### Raw SQL #################################
    products = product.objects.raw('SELECT * FROM shop_product')
    cat = request.GET.get('category', 'products') #### fetching data from webpage
    searchcat = request.GET.get('search', 'products')
    productlist = []
    prods = set()
    ##########################search bar###########################
    if(cat != 'products'):
        for items in products:
            if(items.category == cat):
                productlist.append(items)
    elif(searchcat != 'products'):
        for items in products:
            if(items.subcategory.lower().find(searchcat.lower()) != -1):
                prods.add(items)
            elif(items.category.lower().find(searchcat.lower()) != -1):
                prods.add(items)
            elif(items.product_name.lower().find(searchcat.lower()) != -1):
                prods.add(items)
        for items in prods:
            productlist.append(items)
    ####################################################################################
    customers=request.session.get("customer")
    custom=serializers.deserialize("json", customers) ## deserializing json 
    name=""
    if customers != None:
        for items in custom:
            name=items.object.customer_name
    ###################################################################################
    params = {"products": productlist, "category": cat,"currentuser":name,"categories":categor}
    return render(request, 'shop/categories.html', params)


def mycart(request):

    products = product.objects.raw('SELECT * FROM shop_product')
    catemp = product.objects.raw('select category,id from shop_product')
    categories = set()
    for items in catemp:
        categories.add(items.category)
    categ = []
    for idx, item in enumerate(categories):
        categ.append({item: []})
        for ele in products:
            if(list(categ[idx].keys())[0] == ele.category):
                categ[idx][list(categ[idx].keys())[0]].append(ele)
    categor = []
    for items in categories:
        categor.append(items)


    customers=request.session.get("customer")
    custom=serializers.deserialize("json", customers) ## deserializing json 
    name=""
    if customers != None:
        for items in custom:
            name=items.object.customer_name
    params = {"currentuser":name}
    params["categories"]=categor
    return render(request,"shop/mycart.html",params)


def sale(request):
    products = product.objects.raw('SELECT * FROM shop_product')
    catemp = product.objects.raw('select category,id from shop_product')
    categories = set()
    for items in catemp:
        categories.add(items.category)
    categ = []
    for idx, item in enumerate(categories):
        categ.append({item: []})
        for ele in products:
            if(list(categ[idx].keys())[0] == ele.category):
                categ[idx][list(categ[idx].keys())[0]].append(ele)
    categor = []
    for items in categories:
        categor.append(items)
    ################################RAW SQL###########################
    products = product.objects.raw('SELECT * FROM shop_product')
    cat = request.GET.get('category', 'default')
    dispro=[]
    for items in products:
        if(items.discount>0):
            dispro.append(items)
    ##########################################################################
    customers=request.session.get("customer")
    custom=serializers.deserialize("json", customers) ## deserializing json 
    name=""
    if customers != None:
        for items in custom:
            name=items.object.customer_name
    ###########################################################################
    params={"dispro":dispro,"currentuser":name,"category": cat,"categories":categor}
    return render(request,"shop/sale.html",params)

@csrf_exempt
def handelrequest(request):
    # paytm will sdoneend you post request here
    Checksum=0
    form = request.POST
    response_dict={}
    for i in form.keys():
        response_dict[i] = form[i]
        if (i == 'CHECKSUMHASH'):
            Checksum = form[i]
    
    verify =checksum.verify_checksum(response_dict,MERCHANT_KEY,Checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print("Order Successful")
        else:
            print('Order was not Successful because'+ response_dict['RESPMSG'])
    return render(request,"shop/paymentstatus.html",{'response':response_dict})
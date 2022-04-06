import re
from django.shortcuts import render,redirect
from django.http import HttpResponse
from matplotlib.style import context
from django.contrib import messages
from django.contrib.auth.models import Group

from django.contrib.auth import authenticate, logout,login
from .models import *
from .forms import CustomerForm, OrderForm, AdditemForm, ProductForm
from .filters import OrdrFilter
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only


from django.core.mail import send_mail
from django.conf import settings

import json
from django.http import JsonResponse
import datetime


@unauthenticated_user
def registerpage(request):
    
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        number = request.POST['mobile_number']
        address = request.POST['address']
        city = request.POST['city']
        
        if len(password) <8:
            messages.error(request,'Password is too short')
            return redirect('register')
            
        if password1 == password:
            
            try:
                user = User.objects.get(username = username)
                messages.success(request, 'Username already exists try another one')
                return redirect('register')
            except User.DoesNotExist:

                myuser = User.objects.create_user(username = username,email = email,password = password)
                myuser.number = number
                myuser.address = address
                myuser.city = city
                myuser.save()
                
                group = Group.objects.get(name = 'customer')
                myuser.groups.add(group)
                
                Customer.objects.create(
                    user = myuser,
                    name = myuser.username,
                    phone = myuser.number,
                    email = myuser.email,
                    
                    # phone = instance.mobile_number
                )
                
                subject = 'Thank you for using'
                message = 'Welcome to OSP! we are very proud to have you'
                from_email = settings.EMAIL_HOST_USER
                print(myuser.email)
                to_list = [myuser.email, 'bijjamchennakesavareddy@gmail.com']
                # send_mail(subject, message, from_email, to_list, fail_silently= True)
                
                
                    
                messages.success(request, 'Customer Account created for '+username)
                return redirect('login')
            
        else:
            messages.success(request, 'Passwords did not match')
            return redirect('register')
            
            
        
            
        
            
    context = {}
    return render(request,'accounts/register.html', context)

def register_manager(request):
    
    
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        number = request.POST['mobile_number']
        address = request.POST['address']
        gender = request.POST['gender']
        dob = request.POST['DOB']
        
        if password1 == password:
            
            try:
                user = User.objects.get(username = username)
                messages.success(request, 'Username already exists try another one')
                return redirect('register')
            except User.DoesNotExist:
        
       
                myuser = User.objects.create_user(username = username,email = email,password = password)
                myuser.number = number
                myuser.address = address
                # myuser.gender = gender
                # myuser.dob = dob
                myuser.save()
                
                group = Group.objects.get(name = 'manager')
                myuser.groups.add(group)
                
                Manager.objects.create(
                    user = myuser,
                    name = myuser.username,
                    phone = myuser.number,
                    email = myuser.email,
                    # phone = instance.mobile_number
                )
                
                messages.success(request, 'Manager Account created for '+username)
                
                return redirect('login')
        else:
            messages.success(request, 'Passwords did not match')
            return redirect('register')

    
    context = {}
    return render(request,'accounts/mregister.html', context)


def register_seller(request):
    
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        number = request.POST['mobile_number']
        address = request.POST['address']
        city = request.POST['city']
        
        if password1 == password:
            
            try:
                user = User.objects.get(username = username)
                messages.success(request, 'Username already exists try another one')
                return redirect('register')
            except User.DoesNotExist:
                    
                myuser = User.objects.create_user(username = username,password = password)
                myuser.number = number
                myuser.email = email
                myuser.address = address
                myuser.city = city
                myuser.save()
                
                group = Group.objects.get(name = 'seller')
                myuser.groups.add(group)
                
                Seller.objects.create(
                    user = myuser,
                    name = myuser.username,
                    phone = myuser.number,
                    email = myuser.email,
                    
                    # phone = instance.mobile_number
                )
                
                
                    
                messages.success(request, 'Seller Account created for '+username)
                
                return redirect('login')
        else:
            messages.success(request, 'Passwords did not match')
            return redirect('register')
                
            
    context = {}
    return render(request,'accounts/seller.html', context)



@unauthenticated_user
def loginpage(request):
    
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username = username, password = password) 
        
        if user is not None:
            login(request,user)
            return redirect('managerdashboard')
        else:
            messages.info(request,'Username or password is incorrect')
        
    context = {}
    return render(request,'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    sellers = Seller.objects.all()
    
    total_orders = orders.count()
    total_customers = customers.count()
    
    delivered = orders.filter(status = 'Delivered').count()
    pending  = orders.filter(status = 'Pending').count()
    
    
    context = {'orders' : orders, 'customers' : customers, 'sellers': sellers, 'total_orders':total_orders,'total_customers':total_customers,
               'delivered':delivered ,'pending':pending}
    return render(request, 'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def seller_home(request):
    context = {}
    return render(request, 'accounts/sellerhome.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def seller_inventory(request):
    
    products = request.user.seller.product_set.all()
    context = {'products': products}
    return render(request, 'accounts/seller_Inventory.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def seller_additem(request):
    
    seller=request.user.seller
    
    if request.method == 'POST':
        
        itemname = request.POST['itemname']
        itemcategory = request.POST['itemcategory']
        itemcity = request.POST['itemcity']
        itemdesc = request.POST['itemdesc']
        itemprice = request.POST['itemprice']
        itemimage = request.POST['itemimage']
        
        product = Product.objects.create()
        
        product.Seller = request.user.seller
        product.name = itemname
        product.price = itemprice
        product.category = itemcategory
        product.city = itemcity
        product.description = itemdesc
        product.image = itemimage
        
        product.save()
        
        # print(product)
        
    
        
    context = {}
    return render(request, 'accounts/seller_Add_Item.html', context)




@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    
    total_orders = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending  = orders.filter(status = 'Pending').count()
    
    
    context = {'orders' : orders, 'total_orders':total_orders,
               'delivered':delivered ,'pending':pending}
    return render(request, 'accounts/user.html',context)

@allowed_users(allowed_roles=['customer', 'manager'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance= customer)
        
        if form.is_valid():
            form.save()
            
    
    context = {'form':form}
    
    return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['manager','seller'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html',{'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['manager'])
def customer(request,test_id):
    customer = Customer.objects.get(id = test_id)
    orders = customer.order_set.all()
    orders_count = orders.count()
    
    myFilter = OrdrFilter(request.GET,queryset= orders)
    orders = myFilter.qs
    
    context = {'customer':customer,'orders':orders,'orders_count':orders_count,'myFilter':myFilter}
    return render(request, 'accounts/customer.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager'])
def createOrder(request):
    
    form = OrderForm()
       
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
            
         
    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def addprod(request):
    form = AdditemForm()
    
    if request == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sellerhome')
        
    
    context = {'form':form}
    
    return render(request, 'accounts/seller_additem2.html', context)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def search(request):

    if request.method=="POST":

        searched=request.POST['searched']

        data=Product.objects.filter(name__contains=searched).order_by('-id')

        return render(request, 'accounts/search.html',{'searched':searched,'data':data})

    else:

        return render(request, 'accounts/search.html',{})

# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['manager'])
def updateOrder(request,test_id):
    
    order = Order.objects.get(id = test_id)
    form = OrderForm(instance=order)
    
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form':form}
    
    
    return render(request,'accounts/order_form.html',context)

@allowed_users(allowed_roles=['manager', 'seller'])
def update_prod(request, test_id):
    
    product = Product.objects.get(id = test_id)
    form = ProductForm(instance= product)
    
    if request.method == 'POST':
        
        form = ProductForm(request.POST, instance= product)
        group = request.user.groups.all()[0].name
        if form.is_valid():
            form.save()
            
            if group == 'manager':
                return redirect('managerdashboard')
            if group == 'seller':
                return redirect('sellerhome')
            
            
            # return redirect('sellerhome')
        
    
    context = {'form':form}
    
    return render(request, 'accounts/prod_form.html', context)


def view_prod(request, test_id):
    
    product = Product.objects.get(id = test_id)
    
    context = {'product':product}
    
    return render(request, 'accounts/view_prod.html', context)

def seller_view(request, test_id):
    
    product = Product.objects.get(id = test_id)
    
    context = {'product':product}
    
    return render(request, 'accounts/seller_view.html', context)
        

@login_required(login_url='login')
@allowed_users(allowed_roles=['manager'])
def deleteOrder(request, test_id):
     
    order = Order.objects.get(id = test_id)
    context = {'item':order}
    
    if request.method == 'POST':
        order.delete()
        return redirect('/')
        
    return render(request,'accounts/delete.html',context)

@allowed_users(allowed_roles=['manager', 'seller'])
def delete_product(request, test_id):
    
    product = Product.objects.get(id = test_id)
    group = request.user.groups.all()[0].name
    
    context = {'product':product}
    
    context = {'item':product}
    
    if request.method == 'POST':
        product.delete()
        
        if group == 'manager':
                return redirect('managerdashboard')
        if group == 'seller':
                return redirect('sellerhome')
        
        
        
        # return redirect('sellerhome')
    
    return render(request, 'accounts/deleteprod.html', context)


def seller_account(request):
    
    context = {}
    return render(request, 'accounts/selleraccount.html', context)
    
    
    
    


@allowed_users(allowed_roles=['customer'])
def buyer(request):
    context={}
    return render(request, 'accounts/buyer.html',context)


def item(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(Customer=customer,complete=False)
        items=order.orderitem_set.all()
    else:
        items=[]
        orders={'get_cart_total':0,'get_cart_items':0,'shipping':False}
    products=Product.objects.all()
    context = {'products':products}
    return render(request, 'accounts/item.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(Customer=customer,complete=False)
        items=order.orderitem_set.all()
    else:
        items=[]
        orders={'get_cart_total':0,'get_cart_items':0,'shipping':False}

    context = {'items':items, 'order':order}
    return render(request, 'accounts/cart.html',context)
   

def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(Customer=customer,complete=False)
        items=order.orderitem_set.all()
    else:
        items=[]
        orders={'get_cart_total':0,'get_cart_items':0,'shipping':False}

    context = {'items':items, 'order':order}
    return render(request, 'accounts/checkout.html',context)

def myaccount(request):
    
    customer=request.user.customer
    orders = customer.order_set.all()
    
    print(orders)
    
    context = {'orders':orders}
    return render(request, 'accounts/myaccount.html', context)



def updateitem(request):
    
    data=json.loads(request.body)
    prodID=data['prodID']
    action=data['action']
    print('action:',action)
    print('prodID:',prodID)

    customer=request.user.customer
    product=Product.objects.get(id=prodID) 
    order,created=Order.objects.get_or_create(Customer=customer,complete=False)
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)
    if action=='add':
        orderItem.quantity=(orderItem.quantity+1)
    elif action=='remove':
        orderItem.quantity=(orderItem.quantity-1)
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    
    return JsonResponse('item added',safe=False)

def processorder(request):
    transactionid=datetime.datetime.now().timestamp()
    data=json.loads(request.body)

    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(Customer=customer,complete=False)
        total=float(data['form']['total'])
        order.transactionid=transactionid

        if total==order.get_cart_total:
            order.complete=True
        order.save()
    
        if order.shipping==True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
                
            )
    else:
        print('Login to continue')
    return JsonResponse('payment done',safe=False)

@admin_only
def managerdashboard(request):
    
    customers = Customer.objects.all()
    sellers = Seller.objects.all()
    products = Product.objects.all()
    total_customers = customers.count()
    total_sellers = sellers.count()
    orders = Order.objects.all()
    
    context = {'customers':customers, 'sellers':sellers, 'total_customers': total_customers, 'total_sellers': total_sellers, 'orders': orders, 'products':products}
    
    
    return render(request, 'accounts/manager_view.html', context)

@admin_only
def accountmanager(request):
    
    context = {}
    return render(request, 'accounts/myaccount_manager.html', context)

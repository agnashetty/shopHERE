from email import message
from itertools import product
from math import prod
from unicodedata import category
from urllib import request
from django.shortcuts import redirect, render
from django.views import View
from .models import Cart, Customer, Product, Orderplaced
from .forms import RegistrationForm, profile
from django.db.models import Q
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class home(View):
    def get(self, request):
        western = Product.objects.filter(category = 'W')
        traditional = Product.objects.filter(category = 'T')
        laptops = Product.objects.filter(category = 'L')
        mobiles = Product.objects.filter(category = 'M')

        return render(request, 'app/home.html', {'western_wear': western, 'traditional_wear': traditional, 'laptops': laptops, 'mobiles': mobiles})

class ProductDetail(View):
    def get(self, request, pk):
        productdetail = Product.objects.get(pk= pk)
        item_already_in_cart = False
        item_already_in_cart = Cart.objects.filter(Q(product= productdetail.id)& Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product_detail': productdetail, 'item_already_in_cart': item_already_in_cart} )

@login_required
def add_to_cart(request):
    User = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id= product_id)
    Cart(user=User, product= product).save()
    return redirect("/cartpage")

@login_required
def cartpage(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user= user)
        amount = 0.0
        shipping_charge = 40.0
        total_amount = 0.0
        cart_products = [ p for p in Cart.objects.all() if p.user==user  ]
        if cart_products:
            for p in cart_products:
                single_prod_cost = (p.quantity * p.product.selling_price)
                amount = amount + single_prod_cost
                total_amount = amount + shipping_charge
            return render(request, 'app/cartpage.html', {'total_amount': total_amount , 'amount': amount, 'carts': cart})
        else:
            return render(request, 'app/emptycart.html')
    # return render(request, 'app/cartpage.html', {'carts': cart})

def pluscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product= prod_id) & Q(user = request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_charge = 40.0
        total_amount = 0.0
        
        cart_products = [ p for p in Cart.objects.all() if p.user == request.user  ]
        for p in cart_products:
            single_prod_cost = ( p.quantity * p.product.selling_price )
            amount = amount + single_prod_cost
            total_amount = amount 

        data = {
                    'quantity': c.quantity,
                    'amount' : amount,
                    'total_amount' : total_amount + shipping_charge
                }
    return JsonResponse(data)


def minuscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product= prod_id) & Q(user = request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_charge = 40.0
        total_amount = 0.0
        
        cart_products = [ p for p in Cart.objects.all() if p.user == request.user  ]
        for p in cart_products:
            single_prod_cost = ( p.quantity * p.product.selling_price )
            amount = amount + single_prod_cost
            total_amount = amount 
        data = {
                    'quantity': c.quantity,
                    'amount' : amount,
                    'total_amount' : total_amount + shipping_charge
                }
    return JsonResponse(data)


def removeproduct(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product= prod_id) & Q(user = request.user))
        c.delete()
        amount = 0.0
        shipping_charge = 40.0
        total_amount = 0.0
        
        cart_products = [ p for p in Cart.objects.all() if p.user == request.user  ]
        for p in cart_products:
            single_prod_cost = ( p.quantity * p.product.selling_price )
            amount = amount + single_prod_cost
            total_amount = amount 
        data = {
                    
                    'amount' : amount,
                    'total_amount' : total_amount + shipping_charge
                }
    return JsonResponse(data)


@login_required       
def checkout(request):
    user = request.user
    address = Customer.objects.filter(user = user)
    amount = 0.0
    shipping_charge = 40.0
    total_amount = 0.0
    cart_items = Cart.objects.filter(user = user) 
    cart_products = [ p for p in Cart.objects.all() if p.user == request.user  ]
    if cart_products:
        for p in cart_products:
            single_prod_cost = ( p.quantity * p.product.selling_price )
            amount = amount + single_prod_cost
        total_amount = amount + shipping_charge
    return render(request, 'app/checkout.html', {'add':address, 'total_amount': total_amount, 'cart_items': cart_items})

@login_required
def paymentdone(request):
    user = request.user
    cusid = request.GET.get('custid')
    customer = Customer.objects.get(id=cusid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        Orderplaced(user=user, customer=customer, product= c.product, quantity= c.quantity).save()
        c.delete()
    return redirect("/orders")

@login_required
def orders(request):
    op = Orderplaced.objects.filter(user = request.user)
    return render(request, 'app/orders.html', {'op':op})
    

def buy_now(request):
 return render(request, 'app/buynow.html')


@method_decorator(login_required, name="dispatch")
class Profile(View):
    def get(self, request):
        form = profile()
        return render(request, 'app/profile.html', {'form' : form, 'active': 'btn-primary'})
    
    def post(self, request):
        form = profile(request.POST)
        if form.is_valid():
            User = request.user
            name = form.cleaned_data['name']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            locality = form.cleaned_data['locality']
            zipcode = form.cleaned_data['zipcode']
            data = Customer(user = User, name= name, state=state, city=city, locality=locality, zipcode=zipcode )
            data.save()
        return render(request, 'app/profile.html', {'form' : form, 'active': 'btn-primary'})



def address(request):
    addr = Customer.objects.filter(user= request.user)
    return render(request, 'app/address.html', {'address': addr, 'active': 'btn-primary'})



def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    if data == None:
        mobile = Product.objects.filter(category= 'M')
    return render(request, 'app/mobile.html', {'mobiles': mobile})

def western(request,data=None):
    if data == None:
        western = Product.objects.filter(category= 'W')
    return render(request, 'app/western.html', {'western': western})

def laptop(request,data=None):
    if data == None:
        laptop = Product.objects.filter(category= 'L')
    return render(request, 'app/laptop.html', {'laptop': laptop})

def traditional(request,data=None):
    if data == None:
        traditional = Product.objects.filter(category= 'T')
    return render(request, 'app/traditional.html', {'traditional': traditional})

def login(request):
 return render(request, 'app/login.html')

def signup(request):    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            message.success(request, 'Registered succesfully!')
            form.save()
        return render(request, 'app/signup.html', {'form': form})
    else :
        form = RegistrationForm()
    return render(request, 'app/signup.html', {'form': form})



    
    

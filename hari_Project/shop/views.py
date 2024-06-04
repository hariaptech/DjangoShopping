from django.http import  JsonResponse
from django.shortcuts import redirect, render
from shop.form import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse




def home(request):
    product=Product.objects.filter(trending=1)
    return render(request,'shop/layouts/index.html',{'product':product})

def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
           
            messages.success(request,'Registration Success You Can Login Now ...')
            return redirect('/login')
    return render(request,'shop/layouts/register.html',{'form':form })

def login_page(request):
    if request.method=='POST':
        name=request.POST['username']
        pwd=request.POST['password']
        user=authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            email=user.email 
            send_mail(
                    'login notification',
                    'you have successfully logged in to your account', 
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
            messages.success(request,"Login Successfully")
            return redirect('/')
        else:
            messages.error(request,"Invalid User Name or Password")
            return redirect('/login')
    return render(request,'shop/login.html')

def logout_page(request):
   
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logout Successfully")
        return redirect('home')

def add_to_cart(request):
    if request.headers.get("x-requested-with")=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=(data['product_qty'])
            product_id=(data['pid'])
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Card.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':"Product Already in Card"},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Card.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':"Product Add To Card Success"},status=200)
                    else:
                       return JsonResponse({'status':"Product Stock out "},status=200)
        else:
            return JsonResponse({'status':"Login To Add Card"},status=200)

    else:
        return JsonResponse({'status':"Invalid Access"},status=200)

def collections(request):
    catagory =Catagory.objects.filter(status=0)
    return render(request,'shop/layouts/collections.html',{'catagory':catagory})

def buy_page(request):
        print(request.POST)
        pid = request.POST.get('pid')
        product =Product.objects.get(id=pid)
        qty =int(request.POST.get('qty'))
        total =qty*product.selling_price
        print(product.selling_price)
        return render(request,'shop/products/buy.html',{'total':total,'product':product,'qty':qty})
    
def Payment_success(request,name,qty):
    product =Product.objects.get(name=name)
    product.quantity=product.quantity-qty
    product.save()
    messages.success(request,"Payment Successfully")
    return redirect('/')
   
def collectionsview(request, name):
 
    if Catagory.objects.filter(name=name,status=0):
        pro=Product.objects.filter(catagory__name=name) 
        return render(request,'shop/products/index.html', {'products':pro ,'catagory_name':name})
    else:
        messages.warning(request,'No Such Catagory Found')
        return redirect('collections')

def product_details(request, cname, pname):
    if (Catagory.objects.filter(name=cname,status=0)):
         if (Product.objects.filter(name=pname,status=0)):
             product= Product.objects.filter(name=pname, status=0).first()
             return render(request,'shop/products/product_details.html',{"product":product})
         else:
            messages.warning(request,'No Such Catagory Found')
            return redirect('collections')
    
    else:
        messages.warning(request,'No Such Catagory Found')
        return redirect('collections')
    
def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=data['pid']
            product_status=Product.objects.get(id=product_id)
        if product_status:
            if Favourite.objects.filter(user=request.user.id,product_id=product_id):
                return JsonResponse({'status':'Product Already in Favourite'}, status=200)
            else:
                Favourite.objects.create(user=request.user,product_id=product_id)
                return JsonResponse({'status':'Product Added to Favourite'}, status=200)
        else:
            return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
       return JsonResponse({'status':'Invalid Access'}, status=200)
    
def cart_page(request):
    if request.user.is_authenticated:
        cart=Card.objects.filter(user=request.user)
        return render(request, 'shop/products/cart.html', {'cart':cart})
        
    else:
        return redirect('/')

def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"shop/fav.html",{"fav":fav})
  else:
    return redirect("/")

def remove_cart(request,cid):
  cartitem=Card.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")

def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")
    
# def mail(request):
#     subject = 'The message will be sent '
#     message = 'Thankyou for comming'
#     email_from =settings.EMAIL_HOST_USER
#     recipient_list = ['harishbala354@gmail.com']
#     send_mail(subject, message, email_from,recipient_list)
#     return render(request, 'shop/products/email.html')
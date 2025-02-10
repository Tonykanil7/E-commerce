from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
import razorpay
from django.contrib.auth import login

from shop.models import Product
from cart.models import Cart,Payment,Order_details
from django.contrib.auth.models import User

# Create your views here.
@login_required
def addtocart(request,i):
    user=request.user
    product=Product.objects.get(id=i)
    try:
        if(product.stock>0):
            c=Cart.objects.get(user=user,product=product)
            c.quantity+=1
            product.stock-=1
            c.save()
            product.save()
    except:
        if (product.stock > 0):
            c = Cart.objects.create(user=user, product=product, quantity=1)
            product.stock -= 1
            c.save()
            product.save()
    return redirect('cart:cartview')
@login_required
def cartview(request):
    user=request.user
    c=Cart.objects.filter(user=user)
    total=0
    for i in c:
        total+=i.quantity*i.product.price
    context={'cart':c,'total':total}
    return render(request,'cartview.html',context)

def cartdecrement(request,i):
    user = request.user
    product = Product.objects.get(id=i)
    try:
            c = Cart.objects.get(user=user, product=product)
            if c.quantity>1:
                c.quantity -= 1
                c.save()
                product.stock += 1
                product.save()
            else:
                c.delete()
                product.stock+=1
                product.save()

    except:
        pass
    return redirect('cart:cartview')


def cartdelete(request, i):
    user = request.user
    product = Product.objects.get(id=i)
    try:
        c = Cart.objects.get(user=user, product=product)
        if c.quantity >= 1:
            c.delete()
            product.stock += c.quantity
            product.save()
        else:
            pass

    except:
        pass
    return redirect('cart:cartview')

def orderform(request):
    if request.method=='POST':
        a=request.POST['a']
        p = request.POST['p']
        pc = request.POST['pc']

        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.quantity*i.product.price
        total=int(total)


        client=razorpay.Client(auth=('rzp_test_7W7F8pjzOFlOYf','2DdXYbteICnZcBtJQbxvsj42'))
        response_payment=client.order.create(dict(amount=total*100,currency='INR'))
        print(response_payment)

        order_id=response_payment['id']
        status=response_payment['status']
        if status=='created':
            pa=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            pa.save()

            for i in c:
                o=Order_details.objects.create(product=i.product,user=i.user,no_of_items=i.quantity,address=a,phone=p,pin=pc,order_id=order_id)
                o.save()
            context={'payment':response_payment,'name':u.username}
            return render(request,'payment.html',context)

    return render(request,'orderform.html')

@csrf_exempt
def status(request,n):
    # to avoid logout
    user=User.objects.get(username=n)
    login(request,user)

    #retrieves payment details
    response=request.POST
    print(response)

    # To check the validity of razorpay payment by application
    param_dict={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature'],
    }

    client=razorpay.Client(auth=('rzp_test_7W7F8pjzOFlOYf','2DdXYbteICnZcBtJQbxvsj42'))
    try:
        status=client.utility.verify_payment_signature(param_dict)

        print(status)

        # To add values in payment & order table that where empty
        pa = Payment.objects.get(order_id=response['razorpay_order_id'])
        pa.paid = True
        pa.razorpay_payment_id = response['razorpay_payment_id']
        pa.save()
        o = Order_details.objects.filter(order_id=response['razorpay_order_id'])
        for i in o:
            i.payment_status = 'completed'
            i.save()
        c=Cart.objects.filter(user=user)
        c.delete()
    except:
        pass

    return render(request,'status.html')

def orderview(request):
    u=request.user
    o=Order_details.objects.filter(user=u,payment_status='completed')
    context={'orders':o}
    return render(request,'orderview.html',context)
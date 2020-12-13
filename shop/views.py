from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import Category, Product, Order, OrderItem
from account.models import Profile, User, HereUrPayment, MyTransaction

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.utils import timezone
from account.forms import CreateUserForm, TransactionForm
from django.contrib.auth.forms import UserCreationForm
#from account.forms import TransactionForm

#from shop.models import unique_order_id_generator
import random

def get_user_pending_order(request):
    user_profile = get_object_or_404(User, username=request.user)
    user_order = Order.objects.filter(owner=user_profile, is_ordered=False)
    print(user_profile)
    print(user_order)
    if user_order.exists():
        return user_order[0]
    return 0

def shop_page(request, **kwargs):
    category = Category.objects.all()
    products = Product.objects.filter(is_draft=False)
    #existing_order = get_user_pending_order(request)
    #existing_order = OrderItem.objects.filter(owner=request.user)
    #user_order = User.objects.filter(username=request.user).first()
    #existing_order = OrderItem.objects.all(owner=user_order())
    existing_order = OrderItem.objects.all()
    #existing_order = get_user_pending_order(request)
    TotalOfexisting_order = OrderItem.objects.all().count()
    context = {
        'category': category,
        'products': products,
        'existing_order': existing_order,
        'TotalOfexisting_order': TotalOfexisting_order
    }
    return render(request, 'shop/shop.html', context)

def product_details(request, product_id):
    product_details = Product.objects.get(id=product_id)
    ctg = Category.objects.get(name=product_details.category)
    related_products = Product.objects.filter(category=ctg)[:4]
    existing_order = OrderItem.objects.all()
    TotalOfexisting_order = OrderItem.objects.all().count()
    context = {
        'product': product_details,
        'related_products': related_products,
        'existing_order': existing_order,
        'TotalOfexisting_order': TotalOfexisting_order
    }
    return render(request, 'shop/product-details.html', context)

@login_required(login_url='home')
def add_to_cart(request, item_id):
    # get the user profile
    #username_profile = get_object_or_404(User, pk=item_id)
    #print(username_profile)
    #print('--------------')
    user_profile = get_object_or_404(User, username=request.user)
    #print(user_profile)
    # filter products by id
    product = Product.objects.get(id=item_id)
    #print(product)
    # check if the user already owns this product
    #if product in request.user.profile.ebooks.all():
    #    messages.info(request, 'You already own this ebook')
    #    return redirect(reverse('products:shop')) 
    # create orderItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(product=product)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # generate a reference code
        #rno = random.randint(100000, 999999)
        #user_order.ref_code = rno
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('shop'))

@login_required(login_url='home')
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('shop'))

@login_required(login_url='home')
def order_summary_page(request, **kwargs):
    form = TransactionForm()
    if request.method =="POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()

    user_profile = get_object_or_404(User, username=request.user)
    existing_order_order = Order.objects.get(owner=user_profile, is_ordered=False)
    existing_order = OrderItem.objects.all()
    context = {
        'existing_order': existing_order,
        'existing_order_order': existing_order_order,
        'form':form
    }
    return render(request, 'shop/order-summary.html', context)

def processthepayment(request, order_ref):
    order_to_pay = Order.objects.filter(ref_code=order_ref)
    for object in order_to_pay:
        object.is_ordered=True
        object.save()
        messages.info(request, "Payment completed")
    return redirect(reverse('shop'))
    
def checking_page(request, ref_code):
    order_to_pay_true = Order.objects.filter(ref_code=ref_code, is_ordered=True)
    if order_to_pay_true.exists():
        messageTrue = 'Payment Completed'
        context = {'messageTrue':messageTrue}
        return render(request, 'shop/checking_page.html', context)
    else:
        messageTrue = 'Payment Completed'
        context = {'messageTrue':messageTrue}
        return render(request, 'shop/checking_page.html', context )
 


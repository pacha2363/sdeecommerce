from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .forms import CreateUserForm

from shop.models import Category, Product, OrderItem, Order

def home_page(request):
    category = Category.objects.all()
    products = Product.objects.filter(is_draft=False)[:3]
    existing_order = OrderItem.objects.all()
    TotalOfexisting_order = OrderItem.objects.all().count()
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')

    context = {
        'category': category,
        'products': products,
        'existing_order': existing_order,
        'TotalOfexisting_order': TotalOfexisting_order
    }
    return render(request, 'home.html', context)

def page404(request):
    context = {}
    return render(request, 'page404.html', context)
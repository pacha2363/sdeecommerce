from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import CreateUserForm, CreateAccountHereUr

from django.contrib import messages

from account.models import User, Profile, HereUrPayment
#from hereurpayment.models import HereUrPayment
import datetime

@login_required(login_url='home')
def dashboard_page(request):
    context = {}
    return render(request, 'account/dashboard.html', context)

def login_page(request):
    context = {}
    return render(request, 'account/login.html', context)

def logoutUser(request):
    logout(request) 
    return redirect('home')

def register_page(request):
    if request.user.is_authenticated:
        return redirect('myprofile')
    else:
        form = CreateUserForm()
        if request.method =="POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('home')
        
        context = {'form':form}
        return render(request, 'account/register.html', context)

@login_required(login_url='home')
def myprofile_page(request):
    user = get_object_or_404(User, username=request.user)
    hereurlist = HereUrPayment.objects.filter(user=user) 
    #hereurlist = HereUrPayment.objects.all()
    form = CreateUserForm(instance=user)
    context = {
        "form": form,
        'hereurlist': hereurlist
    }
    return render(request, "account/myprofile.html", context)

@login_required(login_url='myprofile')
def createaccount_page(request):
    form = CreateAccountHereUr()
    if request.method =="POST":
        form = CreateAccountHereUr(request.POST)
        if form.is_valid():
            accountnumber = generateUUID()
            userID = User.objects.get(username=request.user).pk
            print('User ID prmary key : ' + str(userID))
            #userID = form.save(commit=False)
            date = datetime.datetime.now()
            form.accountnumber = accountnumber
            form.user = userID
            form.date = date
            form.save()
            messages.success(request, 'HereUr Account was created ')
            return redirect('myprofile')

    context = {'form':form}
    return render(request, "account/createaccount.html", context)
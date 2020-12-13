from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Profile, MyTransaction, HereUrPayment

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'Your Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email adress'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password from numbers and letters of the Latin alphabet'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'})
        }

class TransactionForm(forms.ModelForm):
    class Meta():
        model = MyTransaction
        fields = ['accountnumber', 'user', 'ref_code', 'receiver', 'paymentmethod', 'phone', 'email', 'amoutoftransaction', 'date_transaction']
        widgets = {
            'accountnumber': forms.Select( attrs={'class': 'form-control select'}),
            'user': forms.Select( attrs={'class': 'form-control select'}),
            'ref_code' : forms.Select( attrs={'class': 'form-control select'}),
            'receiver' : forms.TextInput( attrs={'class': 'form-control'}),
            'paymentmethod' : forms.Select( attrs={'class': 'form-control select'}),
            'phone' : forms.TextInput( attrs={'class': 'form-control'}),
            'email' : forms.EmailInput( attrs={'class': 'form-control'}),
            'amoutoftransaction': forms.TextInput( attrs={'class': 'form-control'}),
        }

class CreateAccountHereUr(forms.ModelForm):
    class Meta:
        model = HereUrPayment
        fields = ['amount', 'details', 'accountType']
        widgets = {
            'amount': forms.TextInput( attrs={'class': 'form-control select'}),
            'details': forms.Textarea( attrs={'class': 'form-control select', 'rows':3, 'cols':5}),
            'accountType' : forms.Select( attrs={'class': 'form-control select'}),
        }

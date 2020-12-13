from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

from .models import MyTransaction, Profile

class TransactionForm(forms.ModelForm):
	class Meta:
		model = MyTransaction
		fields = ('accountnumber', 'user', 'ref_code',	'receiver',	'paymentmethod', 'phone', 'email', 'amoutoftransaction','date_transaction')







model 

class MyTransaction(models.Model):
    accountnumber = models.OneToOneField(HereUrPayment, on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ref_code = models.OneToOneField(Order, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=50)
    paymentmethod = models.CharField(max_length=20,choices=MethodPayment, default="Debit")
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    amoutoftransaction = models.IntegerField()
    date_transaction = models.DateTimeField(null=True)

    def __str__(self):
        return f'Transaction {self.ref_code} - {self.accountnumber} of {self.receiver}'+"."
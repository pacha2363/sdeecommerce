from django.db import models

from django.contrib.auth.models import User

from uuid import uuid4

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

from shop.models import Order, Product, OrderItem

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    about = models.TextField()
    photo = models.ImageField(upload_to='author')
    gender_choice = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    gender = models.CharField(choices=gender_choice, max_length=6)
    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class AuthorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

def generateUUID():
    return str(uuid4())

AccountTypes = (
    ('Current', 'Current'),
    ('Saving', 'Saving')
)
MethodPayment = (
    ('HerUr', 'Here Ur'),
    ('Paypal', 'Paypal'),
    ('VisaCard', 'Visa Card')
)

class HereUrPayment(models.Model):
    accountnumber = models.CharField(default=generateUUID, max_length=36, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=200000)
    details = models.TextField()
    accountType = models.CharField(max_length=8, choices=AccountTypes, default="Debit")
    is_active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return self.accountnumber

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.accountnumber)
        canvas = Image.new('RGB', (360, 360), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.accountnumber}'+".png"
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

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
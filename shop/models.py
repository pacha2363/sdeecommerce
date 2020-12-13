from django.db import models
from django.conf import settings

from account.models import User
#from account.models import Profile

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

import random

def unique_order_id_generator(instance):
    order_new_id= random_string_generator()

    Klass= instance.__class__

    qs_exists= Klass.objects.filter(order_id= order_new_id).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return order_new_id

def generateRefCode():
    rno = random.randint(100000, 999999)
    return str(rno)

class Category(models.Model):
    name = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='images_products_category')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images_product')
    price = models.IntegerField()
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_draft = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    def __str__(self):
        return self.product.name

class Order(models.Model):
    ref_code = models.CharField(default=generateRefCode, max_length=15, unique=True, editable=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)
    qr_code = models.ImageField(upload_to='qr_codes_order', blank=True)
    amount = models.IntegerField(default='20000')

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)

    def save(self, *args, **kwargs):
        idorder = f'http://127.0.0.1:8000/shop/processthepayment/{self.ref_code}'
        qrcode_img = qrcode.make(idorder)
        canvas = Image.new('RGB', (480, 480), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-order-{self.ref_code}'+".png"
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


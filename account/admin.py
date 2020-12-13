from django.contrib import admin

from .models import HereUrPayment, MyTransaction

admin.site.register(HereUrPayment)
admin.site.register(MyTransaction)
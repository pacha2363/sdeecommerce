from django.urls import path
from . import views
from .views import (
    add_to_cart,
    delete_from_cart,
    processthepayment
    )

urlpatterns = [
    path('', views.shop_page, name="shop"),
    path('product/<product_id>', views.product_details, name='product-details'),
    path('add-to-cart/<item_id>', add_to_cart, name='add-to-cart'),
    path('delete-from-cart/<item_id>', delete_from_cart, name='delete-from-cart'),
    path('order-summary/', views.order_summary_page, name='order_summary'),
    path('processthepayment/<order_ref>', processthepayment, name='processthepayment'),
    path('checking/<ref_code>', views.checking_page, name='checking'),

]
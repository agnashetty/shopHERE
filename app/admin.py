from django.contrib import admin

from app.models import Customer
from .models import (Customer, Cart, Product, Orderplaced)

# Register your models here.
@admin.register(Customer)
class customeradmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'locality', 'city', 'state', 'zipcode'
    ]


@admin.register(Cart)
class cartadmin(admin.ModelAdmin):
    list_display = [
        'id', 'product', 'quantity'
    ]

@admin.register(Product)
class productadmin(admin.ModelAdmin):
    list_display = [
        'id', 'product_name', 'brand_name', 'selling_price', 'product_img', 'description'
    ]


@admin.register(Orderplaced)
class orderplacedadmin(admin.ModelAdmin):
    list_display = [
        'id', 'customer', 'product', 'quantity', 'status', 'ordered_date'
    ]


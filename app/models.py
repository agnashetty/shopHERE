from itertools import product
from django.db import models
from django.contrib.auth.models import User
from django.views import View

# Create your models here.

states = (

    ('Andaman and Nicobar', 'Andaman and Nicobar'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'), 
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chandigarh', 'Chandigarh'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Dadra and Nagar Haveli ', 'Dadra and Nagar Haveli '),
    ('Daman and Diu ', 'Daman and Diu '),
    ('Delhi', 'Delhi'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu and Kashmir', 'Jammu and Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ( 'Ladakh', 'Ladakh'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Orissa', 'Orissa'),
    ('	Puducherry ', '	Puducherry '),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),

)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    locality = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    zipcode = models.IntegerField()
    state = models.CharField(choices= states, max_length=30)

    def __str__(self):
        return self.name

category_choice = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('W', 'Western Wear'),
    ('T', 'Traditional Wear'),
)

class Product(models.Model):
    category = models.CharField( choices=category_choice, max_length=2)
    product_name = models.CharField(max_length=50)
    cost_price = models.FloatField()
    selling_price = models.FloatField()
    description = models.TextField()
    brand_name = models.CharField(max_length=50)
    product_img = models.ImageField(upload_to = 'productimg')

    def __str__(self):
        return self.product_name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

status_choice = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the way', 'On the way'),
    ('Delivered', 'Delivered'),
    ('Canceled', 'Canceled'),
    ('Returned', 'Returned'),
    ('Refunded', 'Refunded'),
)

class Orderplaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add =True)
    status = models.CharField( choices= status_choice, max_length=30, default="Pending")

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price


    


from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from shop.models import Shop
from staff.models import Staff


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category/')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved')
    ]
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='products/')
    status = models.CharField(max_length=255, choices=CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Order(models.Model):
    ORDER_CHOICES = {
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    }
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    ordered_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, choices=ORDER_CHOICES, default='Pending')

    def __str__(self):
        return self.shop.name

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name



from django.contrib import admin

# Register your models here.
from product.models import Category, Product, Order, OrderProduct

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(OrderProduct)
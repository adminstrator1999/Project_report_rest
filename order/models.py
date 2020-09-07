from product.models import Product
from user.models import Company

from django.db import models
from order.enums import OrderTypes


class Client(models.Model):
    company = models.ForeignKey('product.Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=123)
    type = models.CharField(max_length=123, choices=OrderTypes.choices())


class Order(models.Model):
    company = models.ForeignKey('product.Company', on_delete=models.CASCADE)
    order_types = models.CharField(max_length=123, choices=OrderTypes.choices())
    start_date = models.DateTimeField(auto_now=True)
    deadline = models.DateField()
    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=True, blank=True)
    unpaid_portion = models.IntegerField()


class Order_detail(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()

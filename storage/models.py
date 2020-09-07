from django.db import models
from product.models import Product, Company


class Storage(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    rest = models.IntegerField()
    last_price = models.IntegerField()
    market_price = models.IntegerField(default=last_price)
    total_price = models.IntegerField()

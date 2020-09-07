from django.db import models
from product.enums import MeasureTypes


class Company(models.Model):
    name = models.CharField(max_length=123)

    def __str__(self):
        return self.name


class Category(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=123)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=123)
    measure_type = models.CharField(max_length=100, choices=MeasureTypes.choices())
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name



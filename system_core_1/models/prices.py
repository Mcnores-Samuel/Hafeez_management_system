"""This module contains the YellowPrices class which is used to
store the prices of the products in the system.
"""
from django.db import models
from django.utils import timezone


class YellowPrices(models.Model):
    """This class contains the prices of the products in the system."""
    phone_type = models.CharField(max_length=50, unique=True)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.phone_type
    

class MosesPrices(models.Model):
    """This class contains the prices of the products in the system."""
    phone_type = models.CharField(max_length=50, unique=True)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.phone_type
    

class ChrisMZPrices(models.Model):
    """This class contains the prices of the products in the system."""
    phone_type = models.CharField(max_length=50, unique=True)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.phone_type
    
class Chris25Prices(models.Model):
    """This class contains the prices of the products in the system."""
    phone_type = models.CharField(max_length=50, unique=True)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.phone_type

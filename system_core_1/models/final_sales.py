"""This module contains the model for the final sales table in the database."""

from django.db import models
from .user_profile import UserProfile
from django.utils import timezone


class FinalSales(models.Model):
    """The model for the final sales table.

    Attributes:
        device_name (Charfield): The name of the device.
        model (Charfield): The model of the device.
        final_price (DecimalField): The final price of the device.
        date_sold (DateTimeField): The date the device was sold.
        sold_by (ForeignKey): The user who sold the device.
    """
    device_name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    final_price = models.DecimalField(max_digits=20, decimal_places=2)
    date_sold = models.DateTimeField(timezone.now())
    sold_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

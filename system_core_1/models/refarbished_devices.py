"""This module contains the model for the refarbished devices table
in the database.

Classes:
    RefarbishedDevices: The model for the refarbished devices table.
"""
from django.db import models
from .user_profile import UserProfile
from django.utils import timezone
from django.db.models import F, Sum


class RefarbishedDevices(models.Model):
    """The model for the refarbished devices table.

    Attributes:
        held_by (ForeignKey): The user who holds the device.
        device_name (Charfield): The name of the device.
        model (Charfield): The model of the device.
        total (IntegerField): The total number of devices.
        previous_total (IntegerField): The previous total number of devices.
        cost (DecimalField): The cost of the device.
        original_price (DecimalField): The original price of the device.
        date_added (DateTimeField): The date the device was added.
        date_modified (DateTimeField): The date the device was modified.
    """
    held_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    total = models.IntegerField(default=0)
    previous_total = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=20, decimal_places=2)
    date_added = models.DateTimeField(timezone.now())
    date_modified = models.DateTimeField(timezone.now())

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'refarbished_devices'
        verbose_name = 'Refarbished Device'
        verbose_name_plural = 'Refarbished Devices'

    @classmethod
    def total_cost(cls):
        """Returns the total cost of all devices."""
        total = cls.objects.aggregate(
            total_cost=Sum(F('cost') * F('total')))
        return total['total_cost']


class RefarbishedDevicesSales(models.Model):
    """The model for the refarbished devices sales table.

    Attributes:
        name (Charfield): The name of the device.
        model (Charfield): The model of the device.
        total (IntegerField): The total number of devices sold.
        cost (DecimalField): The cost of the device.
        price_sold (DecimalField): The price the device was sold for.
        profit (DecimalField): The profit made from the sale.
        date_sold (DateTimeField): The date the device was sold.
        sold_by (ForeignKey): The user who sold the device.
    """
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    total = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=20, decimal_places=2)
    price_sold = models.DecimalField(max_digits=20, decimal_places=2)
    profit = models.DecimalField(max_digits=20, decimal_places=2)
    date_sold = models.DateTimeField(timezone.now())
    sold_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'refarbished_devices_sales'
        verbose_name = 'Refarbished Sale'
        verbose_name_plural = 'Refarbished Sales'
#!/usr/bin/env python3
"""This module contains the MainStorage model, which represents the stock
available as part of the main inventory. It includes fields to store relevant
information about each phone, such as the phone type and IMEI number

The MainStorage model represents the primary storage for phones available
in your application. It serves as the central repository for tracking phone
inventory and availability.

The MainStorage model plays a crucial role in managing the availability and
tracking of phones within your application. It helps ensure that phones are in
stock, available for assignment, and properly recorded.

Properly maintaining the MainStorage model is essential for accurate inventory
management.

Changes to the availability or assignment of phones should be reflected in this
model to ensure accurate tracking.

The MainStorage model forms an essential part of the database, enabling
effective management of customer data, tracking interactions, and
maintaining accurate records of customers engaged in your loan-based
phone sales program.
"""
from django.db import models
from .agent_profile import AgentProfile
from django.conf import settings

PHONELIST = (
        ("S18", "S18"), ("A60", "A60"),
        ("A04", "A04"), ("A18", "A18"),
        ("C20", "C20"), ("C19", "C19"),
        ("S10", "S10"), ("10C8G", "10C8G"),
        ("10C", "10C"), ("8C", "8C"),
        ("P7P4G", "P7P4G"), ("P7P3G", "P7P3G"),
        ("P7", "P7"), ("S9", "S9"), ('9T', '9T'),
        ("S8", "S8"), ("S7", "S7"),
    )

class MainStorage(models.Model):
    """This model represent the entire stock available and sold in all posts.

    The MainStorage model represents the primary storage for phones available
    in your application. It serves as the central repository for tracking phone
    inventory and availability.

    Fields:
    - device_imei: The International Mobile Equipment Identity (IMEI) number,
      which serves as a unique identifier for each phone.
    - phone_type: The type or model of the phone.
    - in_stock: A boolean field indicating whether the phone is currently in stock
      and available for sale.
    - assigned: A boolean field indicating whether the phone is currently assigned
      to an agent or customer.
    - stock_out_date: The date on which the phone was purchased or added to the
      inventory.

    Usage:
    The MainStorage model plays a crucial role in managing the availability and
    tracking of phones within your application. It helps ensure that phones are in
    stock, available for assignment, and properly recorded.

    Note:
    - Properly maintaining the MainStorage model is essential for accurate inventory
      management.
    - Changes to the availability or assignment of phones should be reflected in this
      model to ensure accurate tracking.
    """
    device_imei = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=50, null=True)
    phone_type = models.CharField(max_length=25, choices=PHONELIST, default='S18 (4+64)')
    category = models.CharField(max_length=25, null=True)
    spec = models.CharField(max_length=25, null=True)
    screen_size = models.CharField(max_length=25, null=True)
    battery = models.CharField(max_length=25, null=True)
    camera = models.CharField(max_length=25, null=True)
    os = models.CharField(max_length=25, null=True)
    in_stock = models.BooleanField(default=True)
    sales_type = models.CharField(max_length=10, null=True)
    contract_no = models.CharField(max_length=9, null=True)
    entry_date = models.DateField()
    stock_out_date = models.DateField()
    assigned = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    recieved = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['device_imei', 'phone_type', 'in_stock', 'assigned'])
        ]

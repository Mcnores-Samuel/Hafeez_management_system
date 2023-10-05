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

PHONELIST = (
        ("S18 (4+64)", "S18 (4+64)"), ("A60 (2+32)", "A60 (2+32)"),
        ("A04 (2+32)", "A04 (2+32)"), ("A18 (1+32)", "A18 (1+32)"),
        ("Camon 20 (8+256)", "Camon 20 (8+256)"), ("Camon 19 (4+128)", "Camon 19 (4+128)"),
        ("Spark 10 (8+128)", "Spark 10 (8+128)"), ("Spark 10C (8+128)", "Spark 10C (8+128)"),
        ("Spark 10C (4+128)", "Spark 10C (4+128)"), ("Spark 8C (2+64)", "Spark 8C (2+64)"),
        ("Pop 7 pro (4+64)", "Pop 7 pro (4+64)"), ("Pop 7 pro (3+64)", "Pop 7 pro (3+64)"),
        ("Pop 7 (2+64)", "Pop 7 (2+64)"),
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
    phone_type = models.CharField(max_length=25, choices=PHONELIST, default='S18 (4+64)')
    in_stock = models.BooleanField(default=True)
    sales_type = models.CharField(max_length=10, null=True)
    contract_no = models.CharField(max_length=8, null=True)
    entry_date = models.DateField()
    stock_out_date = models.DateField()
    assigned = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['device_imei', 'phone_type', 'in_stock', 'assigned'])
        ]
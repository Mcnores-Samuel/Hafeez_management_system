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
from django.conf import settings
from django.utils import timezone

PHONELIST = (
        ("S18", "S18"), ("A60", "A60"),
        ("A04", "A04"), ("A18", "A18"),
        ("C20", "C20"), ("C19", "C19"),
        ("S10Pro", "S10Pro"),
        ("S10", "S10"), ("10C8G", "10C8G"),
        ("10C", "10C"), ("8C", "8C"),
        ("P7P4G", "P7P4G"), ("P7P3G", "P7P3G"),
        ("P7", "P7"), ("S9", "S9"), ('9T', '9T'),
        ("S8", "S8"), ("S7", "S7"),
    )

category = (
    ("Tecno", "Tecno"),
    ("Itel", "Itel"),
    ("Infinix", "Infinix"),
    ("Redmi", "Redmi"),
)

spec = (
    ("8+256", "8+256"),
    ("4+256", "4+256"),
    ("8+128", "8+128"),
    ("4+128", "4+128"),
    ("4+64", "4+64"),
    ("3+64", "3+64"),
    ("2+64", "2+64"),
    ("3+32", "3+32"),
    ("2+32", "2+32"),
    ("1+32", "1+32"),
    ("2+16", "2+16"),
)

screen_size = (
    ("6.8 inch HD+ display", "6.8 inch HD+ display"),
    ("6.6 inch HD+ display", "6.6 inch HD+ display"),
    ("6.5 inch HD+ display", "6.5 inch HD+ display"),
    ("6.52 inch HD+ display", "6.52 inch HD+ display"),
    ("6.5 inch HD+ display", "6.5 inch HD+ display"),
    ("6.52 inch HD+ display", "6.52 inch HD+ display"),
    ("6.3 inch HD+ display", "6.3 inch HD+ display"),
    ("5.5 inch HD+ display", "5.5 inch HD+ display"),
)

battery = (
    ("6000mAh", "6000mAh"),
    ("5000mAh", "5000mAh"),
    ("4000mAh", "4000mAh"),
    ("3000mAh", "3000mAh"),
    ("2500mAh", "2500mAh"),
    ("2000mAh", "2000mAh"),
    ("1500mAh", "1500mAh"),
    ("1000mAh", "1000mAh"),
)

camera = (
    ("200MP", "200MP"),
    ("160MP", "160MP"),
    ("130MP", "130MP"),
    ("100MP", "100MP"),
    ("80MP", "80MP"),
    ("64MP", "64MP"),
    ("50MP", "50MP"),
    ("48MP", "48MP"),
    ("32MP", "32MP"),
    ("24MP", "24MP"),
    ("16MP", "16MP"),
    ("13MP", "13MP"),
    ("12MP", "12MP"),
    ("8MP", "8MP"),
    ("5MP", "5MP"),
)

OS = (
    ("Android 13", "Android 13"),
    ("Android 12", "Android 12"),
    ("Android 11", "Android 11"),
    ("Android 10", "Android 10"),
    ("Android 9", "Android 9"),
    ("Android 8", "Android 8"),
    ("Android 7", "Android 7"),
)

sales_type = (
    ("##", "##"),
    ("Cash", "Cash"),
    ("Loan", "Loan"),
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
    phone_type = models.CharField(max_length=25, choices=PHONELIST, default='S18')
    category = models.CharField(max_length=25, null=True, choices=category, default='Tecno')
    spec = models.CharField(max_length=25, null=True, choices=spec, default='8+256')
    screen_size = models.CharField(max_length=25, null=True, choices=screen_size, default='6.8 inch HD+ display')
    battery = models.CharField(max_length=25, null=True, choices=battery, default='6000mAh')
    camera = models.CharField(max_length=25, null=True, choices=camera, default='200MP')
    os = models.CharField(max_length=25, null=True, choices=OS, default='Android 13')
    in_stock = models.BooleanField(default=True)
    sales_type = models.CharField(max_length=10, null=True, choices=sales_type, default='##')
    contract_no = models.CharField(max_length=9, null=True)
    entry_date = models.DateField()
    stock_out_date = models.DateField()
    assigned = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    recieved = models.BooleanField(default=False)
    pending = models.BooleanField(default=False)
    missing = models.BooleanField(default=False)
    assigned_from = models.CharField(max_length=50, null=True, blank=True)
    updated_by = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['device_imei', 'phone_type', 'in_stock', 'assigned'])
        ]


DEVICES = (
    ("MIFI", "MIFI"), ("ROUTER (IDU)", "ROUTER (IDU)"),
)

class Airtel_mifi_storage(models.Model):
    """This model represent the entire stock available and sold in all posts
    for airtel mifi and routers

    Fields:
    - device_imei: The International Mobile Equipment Identity (IMEI) number,
      which serves as a unique identifier for each phone.
    device_type: The type or model of the phone.
    - in_stock: A boolean field indicating whether the phone is currently in stock
      and available for sale.
    - assigned: A boolean field indicating whether the phone is currently
      assigned to an agent or customer.
    - stock_out_date: The date on which the phone was purchased or added to the
      inventory.
    """
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    recieved = models.BooleanField(default=False)
    device_imei = models.CharField(max_length=15, unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    device = models.CharField(max_length=25, choices=DEVICES, default='MIFI')
    pending = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    inactive = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    assigned = models.BooleanField(default=False)
    entry_date = models.DateField(default=timezone.now)
    stock_out_date = models.DateField(default=timezone.now)
    cash_recieved = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['device_imei', 'device', 'in_stock', 'assigned'])
        ]
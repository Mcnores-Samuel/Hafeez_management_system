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
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    device_imei = models.CharField(max_length=15, unique=True)
    device_imei_2 = models.CharField(max_length=15, unique=True,
                                     null=True, blank=True)
    name = models.CharField(max_length=50, null=True)
    phone_type = models.CharField(max_length=25, blank=True, null=True)
    category = models.CharField(max_length=25, null=True, default='Tecno')
    spec = models.CharField(max_length=25, null=True, blank=True)
    screen_size = models.CharField(max_length=25, null=True, blank=True)
    battery = models.CharField(max_length=25, null=True, blank=True)
    camera = models.CharField(max_length=25, null=True, blank=True)
    os = models.CharField(max_length=25, null=True, blank=True)
    sales_type = models.CharField(max_length=10, null=True, choices=sales_type, default='##')
    contract_no = models.CharField(max_length=9, null=True, default='##')
    entry_date = models.DateField(default=timezone.now)
    stock_out_date = models.DateField(default=timezone.now)
    collected_on = models.DateField(default=timezone.now)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payg_number = models.CharField(max_length=15, null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    assigned = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    mbo_approved = models.BooleanField(default=False)
    mbo_rejected = models.BooleanField(default=False)
    deposit_paid = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    recieved = models.BooleanField(default=False)
    on_display = models.BooleanField(default=False)
    pending = models.BooleanField(default=False)
    missing = models.BooleanField(default=False)
    faulty = models.BooleanField(default=False)
    issue = models.BooleanField(default=False)
    assigned_from = models.CharField(max_length=50, null=True, blank=True)
    updated_by = models.CharField(max_length=50, null=True, blank=True)
    comment = models.CharField(max_length=256, null=True, blank=True)
    supplier = models.CharField(max_length=50, null=True, blank=True)
    trans_image = models.ImageField(upload_to='Cash_Transactions', null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['device_imei', 'phone_type', 'in_stock', 'assigned'])
        ]

    def __str__(self):
        """String representation of the phone data model"""
        return "Device: {}, Imei: {}".format(self.name, self.device_imei)


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
    DEVICES = (
        ("MIFI", "MIFI"), ("IDU", "IDU"),
      )

    cash_recieved_by = (
        ('Not Paid', 'Not Paid'), ('Sahil', 'Sahil'), ('Suhail', 'Suhail'),
        ('Shehzaad', 'Shehzaad'), ("Sahil's Father", "Sahil's Father")
      )
    
    promoter = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              null=True, blank=True)
    device_imei = models.CharField(max_length=15, unique=True)
    device_phone_no = models.CharField(max_length=15, unique=True, null=True, blank=True)
    device_type = models.CharField(max_length=25, choices=DEVICES, default='MIFI')
    team_leader = models.CharField(max_length=25, null=True, blank=True)
    days_left = models.IntegerField(default=14)
    days_after_due = models.IntegerField(default=0)
    entry_date = models.DateTimeField(timezone.now, default=timezone.now)
    collected_on = models.DateTimeField(timezone.now, default=timezone.now)
    last_updated = models.DateTimeField(timezone.now, default=timezone.now)
    next_due_date = models.DateTimeField(timezone.now, default=timezone.now)
    date_sold = models.DateTimeField(timezone.now, default=timezone.now)
    in_stock = models.BooleanField(default=True)
    activated = models.BooleanField(default=False)
    payment_confirmed = models.BooleanField(default=False)
    data_submitted = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
    returned_by = models.CharField(max_length=25, null=True, blank=True)
    returned_on = models.DateTimeField(timezone.now, default=timezone.now)
    cash_recieved_by = models.CharField(max_length=25, choices=cash_recieved_by, default='Not Paid')
    paid = models.BooleanField(default=False)
    updated_by = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['device_imei',
                                 'device_type', 'in_stock'])
        ]
        verbose_name_plural = 'Airtel Devices'

    def __str__(self):
        """String representation of the phone data model"""
        return "Device: {}| Imei: {}| heldby: {}".format(
            self.device_type, self.device_imei, self.promoter)

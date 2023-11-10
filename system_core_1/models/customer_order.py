#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""Thins module contains the PhoneData model, which represents the phones
purchased by customers. It includes fields to store relevant information about
each phone, such as the phone type and IMEI number
"""
from django.db import models
from .customer_details import CustomerData
from .agent_profile import AgentProfile


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

class PhoneData(models.Model):
    """The PhoneData model establishes a relationship with the Customers and
    Agents models through foreign key fields (customer and agent respectively)
    This allows each phone record to be linked to the corresponding customer
    and agent.

    The model also includes fields to capture specific details about the phone
    purchase, such as phone_type, imei_number, selling_price, cost_price,
    payment_period, and deposit.
    """
    customer = models.ForeignKey(CustomerData, on_delete=models.CASCADE)
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE)
    phone_type = models.CharField(max_length=25, choices=PHONELIST, default='S18')
    imei_number = models.CharField(max_length=15, unique=True)
    contract_number = models.CharField(max_length=9,null=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_period = models.CharField(max_length=50, null=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    class Meta:
        app_label = 'system_core_1'
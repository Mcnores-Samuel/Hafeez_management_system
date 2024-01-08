#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""Thins module contains the PhoneData model, which represents the phones
purchased by customers. It includes fields to store relevant information about
each phone, such as the phone type and IMEI number
"""
from django.db import models
from .customer_details import CustomerData
from .agent_profile import AgentProfile


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
    phone_type = models.CharField(max_length=25, default='S18')
    imei_number = models.CharField(max_length=15, unique=True)
    contract_number = models.CharField(max_length=9, null=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_period = models.CharField(max_length=50, null=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    class Meta:
        app_label = 'system_core_1'
        index_together = ('customer', 'agent')
        ordering = ['-id']
        verbose_name_plural = 'Customer Orders'

    def __str__(self):
        """String representation of the phone data model"""
        return "{} {} {}".format(self.customer, self.phone_type, self.imei_number)
        
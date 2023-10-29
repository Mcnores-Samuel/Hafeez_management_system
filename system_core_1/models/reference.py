#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the PhoneReference model, which serves as a catalog of
phones, including their specifications and pricing information.

The PhoneReference model represents reference data for different phone models
available for sale. It serves as a catalog of phones, including their specifications
and pricing information. This model is essential for managing and organizing the
inventory of phones in your application.
"""
from django.db import models


class Phone_reference(models.Model):
    """This model holds static information on phone's payment methods.

    The PhoneReference model represents reference data for different phone models
    available for sale. It serves as a catalog of phones, including their specifications
    and pricing information. This model is essential for managing and organizing the
    inventory of phones in your application.

    Fields:
    - phone: The name or model of the phone.
    - merchant_price: The price at which the phone is sold to merchants or agents.
    - deposit: The initial deposit amount required for purchasing the phone.

    Usage:
    The PhoneReference model is primarily used for maintaining a centralized database
    of available phone models and their associated details. It allows for easy retrieval
    of phone information when agents or users need to select a phone for sale.

    Note:
    - This model should be populated with relevant phone data, including new phone
      models and their specifications.
    - The data in this model can be used for pricing, cataloging, and displaying phone
      options to agents and customers.
    - Changes to this model can affect the phone selection process in the application,
      so it should be kept up-to-date and accurate.
    """
    phone = models.CharField(max_length=30, unique=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    merchant_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cash_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        app_label = 'system_core_1'
    
    def __str__(self):
        """String representation of the phone reference model"""
        return ("{} {} {}".format(self.phone, self.deposit, self.merchant_price))
    
    @classmethod
    def get_all_phones(cls):
        return cls.objects.all()
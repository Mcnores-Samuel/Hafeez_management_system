#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module contains the special orders model class."""
from __future__ import unicode_literals
from django.db import models
from .user_profile import UserProfile
from django.utils import timezone


class SpecialOrders(models.Model):
    """This class contains the special orders model.

    Attributes:
        presentative (ForeignKey): The representative who made the order.
        created_at (DateTimeField): The date and time the order was made.
        updated_at (DateTimeField): The date and time the order was updated.
        current_orders (CharField): The current orders.
        initial_balance (IntegerField): The initial balance.
        current_balance (IntegerField): The current balance.
        final_balance (IntegerField): The final balance.
    """
    presentative = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    last_payment_date = models.DateTimeField(default=timezone.now)
    current_payment = models.IntegerField(default=0)
    last_payment = models.IntegerField(default=0)
    current_orders = models.IntegerField(default=0)
    initial_balance = models.IntegerField(default=0)
    current_balance = models.IntegerField(default=0)
    final_balance = models.IntegerField(default=0)
    total_paid = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    year = models.IntegerField(default=0)

    class Meta:
        """This class contains the meta data for the special orders model."""
        verbose_name_plural = 'Special Orders'
        
    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "Name: {}, Final Balance: {}".format(self.presentative,
                                                    self.final_balance)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the AgentStock model, which represents the stock
available to agents. It includes fields to store relevant information about
each phone, such as the phone type and IMEI number

The AgentStock model represents the inventory of phones assigned to agents
within the application. It tracks the availability and status of phones
assigned to specific agents.
"""
from django.db import models
from .agent_profile import AgentProfile
from .main_storage import MainStorage


class AgentStock(models.Model):
    """
    The AgentStock model represents the inventory of phones assigned to agents
    within the application. It tracks the availability and status of phones
    assigned to specific agents.

    Fields:
      - agent: A foreign key reference to the AgentProfile of the assigned agent.
      - imei_number: The International Mobile Equipment Identity (IMEI) number of
        the phone, serving as a unique identifier.
      - phone_type: The type or model of the phone.
      - collection_date: The date on which the phone was collected by the agent.
      - sales_type: The type of sale (e.g., cash or loan) for the phone.
      - in_stock: A boolean field indicating whether the phone is currently in stock
        and available for assignment to agents.
    
    Usage:
      The AgentStock model plays a vital role in managing the allocation of phones to
      agents. It helps track which phones are assigned to which agents, their collection
      dates, sales types, and overall availability.

    Note:
    - Properly managing the AgentStock model ensures that agents have access to the
      phones they need for sales.
    - Changes to the assignment, collection, or availability of phones should be
      accurately recorded in this model.
    """
    TYPES = (
        ("Cash", "Cash"),
        ("Loan", "Loan"),
    )
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE)
    imei_number = models.CharField(max_length=15, unique=True)
    phone_type = models.CharField(max_length=25, blank=True)
    collection_date = models.DateField()
    sales_type = models.CharField(max_length=10, choices=TYPES, default="Loan")
    contract_number = models.CharField(max_length=9,null=True)
    in_stock = models.BooleanField(default=True)
    stock_out_date = models.DateField()
    sold = models.BooleanField(default=False)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     """Dynamically populate choices for imei_number from MainStorage"""
    #     self._update_imei_number_choices()

    # def _update_imei_number_choices(self):
    #     in_stock_phones = MainStorage.objects.filter(in_stock=True)
    #     choices = [(phone.device_imei, phone.device_imei) for phone in in_stock_phones]
    #     self._meta.get_field('imei_number').choices = choices

    class Meta:
        indexes = [
            models.Index(fields=['imei_number', 'phone_type', 'in_stock', 'sold'])
        ]
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the AgentStockForm class, which is used to dynamically create
the AgentStock form to allow admin to add phones to their stock
"""
from django import forms
from ..models.agent_stock import AgentStock
from ..models.main_storage import MainStorage


class AgentStockForm(forms.ModelForm):
    """Dynamically populates the phone_type field based on the selected imei_number
    in the Django admin interface when creating or editing an AgentStock instance

    This form is used in the Django admin interface to facilitate the creation
    and editing of AgentStock instances. It dynamically populates the phone_type
    field based on the selected imei_number, ensuring that the phone_type field
    is always consistent with the selected phone.

    Form Fields:
    - agent: Foreign key to the AgentProfile model.
    - imei_number: Unique identification number of the phone.
    - phone_type: Type of the phone.
    - collection_date: Date when the phone was collected by the agent.
    - sales_type: Type of sale (Cash or Loan).
    - in_stock: Boolean field indicating whether the phone is in stock.
    - stock_out_date: Date when the phone was sold or removed from stock.

    Methods:
    - __init__: Initializes the form, sets choices for imei_number based on
        available phones in the MainStorage model, and dynamically sets choices
        for phone_type based on the selected imei_number.
    - clean: Validates the form data and dynamically sets the phone_type field
        based on the selected imei_number.

    Usage:
        This form is used in the Django admin interface to facilitate the creation
        and editing of AgentStock instances. It dynamically populates the phone_type
        field based on the selected imei_number, ensuring that the phone_type field
        is always consistent with the selected phone.
    """
    class Meta:
        model = AgentStock
        fields = ['agent', 'imei_number', 'phone_type', 'collection_date',
                   'sales_type', 'in_stock', 'stock_out_date']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Dynamically populate choices for imei_number from MainStorage"""
        in_stock_phones = MainStorage.objects.filter(in_stock=True, assigned=False).order_by('id')
        choices = [(phone.device_imei, phone.device_imei) for phone in in_stock_phones]
        self.fields['imei_number'].choices = choices

    def clean(self):
        """Retrieves the imei_number entered in the form and use it to fetch the
          associated phone_type from the MainStorage model.
        """
        cleaned_data = super().clean()
        imei_number = cleaned_data.get('imei_number')
        try:
            main_storage = MainStorage.objects.get(device_imei=imei_number, in_stock=True)
            phone_type = main_storage.phone_type
            cleaned_data['phone_type'] = phone_type
        except MainStorage.DoesNotExist:
            pass
        return cleaned_data
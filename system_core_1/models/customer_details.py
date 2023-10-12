#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the CustomerData model, which serves as a central
repository for customer-related information gathered during the phone purchasing
process. Each customer record is uniquely identified by a generated customer_id,
and the associated timestamp indicates when the data was collected.

The CustomerData model serves as a central repository for customer-related
information gathered during the phone purchasing process. Each customer
record is uniquely identified by a generated customer_id, and the
associated timestamp indicates when the data was collected.

Contact information is collected through customer_contact and
second_contact fields, allowing for multiple points of communication.
Witness information is recorded in first_witness_name,
first_witness_contact,second_witness_name, and second_witness_contact
fields to provide additional verification.

Location-related details are captured, including customer_location,
nearest_school, and nearest_market_church_hospital, aiding in logistics
and customer service.

customer_email allows for electronic communication with the customer.
The contract_number links the customer to a specific contract, and referral
captures any relevant referral information.
"""
from django.db import models


class CustomerData(models.Model):
    """The Customers table serves as a central repository for customer-related
    information gathered during the phone purchasing process. Each customer
    record is uniquely identified by a generated customer_id, and the
    associated timestamp indicates when the data was collected.

    Contact information is collected through customer_contact and
    second_contact fields, allowing for multiple points of communication.
    Witness information is recorded in first_witness_name,
    first_witness_contact,second_witness_name, and second_witness_contact
    fields to provide additional verification.

    Location-related details are captured, including customer_location,
    nearest_school, and nearest_market_church_hospital, aiding in logistics
    and customer service.

    customer_email allows for electronic communication with the customer.
    The contract_number links the customer to a specific contract, and referral
    captures any relevant referral information.

    The Customers table forms an essential part of the database, enabling
    effective management of customer data, tracking interactions, and
    maintaining accurate records of customers engaged in your loan-based
    phone sales program.
    """
    created_at = models.DateTimeField(null=True)
    update_at = models.DateTimeField()
    customer_name = models.CharField(max_length=50)
    national_id = models.CharField(max_length=9)
    customer_contact = models.CharField(max_length=13)
    second_contact = models.CharField(max_length=13, null=True)
    first_witness_name = models.CharField(max_length=50)
    first_witness_contact = models.CharField(max_length=13)
    second_witness_name = models.CharField(max_length=50)
    second_witness_contact = models.CharField(max_length=13)
    customer_location = models.CharField(max_length=50)
    nearest_school = models.CharField(max_length=50)
    nearest_market_church_hospital = models.CharField(max_length=50)
    customer_email = models.CharField(max_length=50, null=True)
    working_status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        app_label = 'system_core_1'
        indexes = [
            models.Index(fields=['customer_name', 'national_id', 'customer_contact', 'customer_email']),
        ]
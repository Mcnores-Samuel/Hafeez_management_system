#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the ApproveContracts view, which is responsible for
approving contracts.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models.customer_details import CustomerData
from ..models.main_storage import MainStorage
from ..models.customer_order import PhoneData


@login_required
def approve_contracts(request):
    """Approve contracts.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        customer = CustomerData.objects.get(id=customer_id)
        customer.approved = True
        customer.pending = False
        customer.save()
        messages.success(request, 'Contract approved successfully.')
    return redirect('dashboard')


@login_required
def decline_contracts(request):
    """Decline contracts.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        customer = CustomerData.objects.get(id=customer_id)
        phone = PhoneData.objects.get(customer=customer)
        imei = phone.imei_number
        phone = MainStorage.objects.get(device_imei=imei)
        phone.in_stock = True
        phone.sold = False
        phone.stock_out_date = phone.entry_date
        phone.save()
        customer.approved = False
        customer.pending = False
        customer.rejected = True
        customer.save()
        messages.success(request, 'Contract declined successfully.')
    return redirect('dashboard')

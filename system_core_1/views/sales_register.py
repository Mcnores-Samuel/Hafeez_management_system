#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains combined data collection view function, which is responsible
for handling the collection of customer and phone data during the phone purchasing
process by agents.
"""
from django.shortcuts import render, redirect
from ..forms.customer_data import CombinedDataForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models.user_profile import UserProfile
from ..models.main_storage import MainStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
def combinedData_collection(request, data_id):
    """
    The `combinedData_collection` view function is a Django view responsible for
    handling the collection of customer and phone data during the phone purchasing
    process by agents.

    Functionality:
    - Checks if the user is authenticated and is an agent. Only agents are allowed
      to access this view.
    - Verifies if the agent has available stock of phones.
    - Renders either the combined data form or an "out of stock" message based on
      the agent's stock availability.
    - If the agent has stock and submits the form, customer and phone records are
      created in the database.
    - If the agent is out of stock, a message is displayed, instructing them to
      contact the office for stock replenishment.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - If the user is not authenticated or is not an agent, it returns a 403 Forbidden
      response.
    - If the agent is authenticated and has stock, it renders the combined data form.
    - If the agent is out of stock, it renders an "out of stock" message.

    Usage:
    Agents access this view to collect customer data and select phones for sale.
    It ensures that agents with available stock can proceed with data collection,
    while agents without stock are notified to contact the office for replenishment.

    Note:
    This view assumes user authentication and validation of agent status have been
    handled in the authentication system and AgentProfile model.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='staff_members').exists():
        if request.method == 'POST':
            form = CombinedDataForm(request.POST, user=request.user)
            if form.is_valid():
                payment_method = form.cleaned_data['payment_method']
                if payment_method == 'Cash':
                    sales_item1 = form.process_cash_payment(data_id)
                    messages.success(request, '{} of IMEI {} Successfully sold'.format(
                        sales_item1.name, sales_item1.device_imei))
                    return redirect('dashboard')
                elif payment_method == 'Loan':
                    sales_item = form.process_loan_payment(data_id)
                    if sales_item == 'already sold':
                        messages.warning(request, 'Already sold, please select another device')
                        return redirect('dashboard')
                    messages.success(request, '{} of IMEI {} Successfully sold'.format(
                        sales_item.name, sales_item.device_imei))
                    return redirect('dashboard')
            else:
                messages.warning(request, 'Please correct the errors below')
        else:
            form = CombinedDataForm(user=request.user)
        return render(request, 'registration/collect_customer_data.html', {'form': form})
    else:
        return HttpResponseForbidden("Access Denied")


@login_required
@csrf_exempt
def uploadBulkSales(request):
    """
    The `uploadBulkSales` view function is a Django view responsible for
    handling the bulk upload of sales data by all outlets

    Functionality:
    - Checks if the user is authenticated and is an agent. Only agents are allowed
      to access this view.
    - Verifies if the agent has available stock of phones.
    """
    if request.method == 'POST' and request.user.is_staff and request.user.is_superuser:
        data = request.POST.get('data', None)
        date = request.POST.get('date', None)
        sales_type = request.POST.get('sales_type', None)
        if data:
            scanned_items = json.loads(data)
            date = json.loads(date)
            sales_type = json.loads(sales_type)
            not_in_stock = []
            for item in scanned_items:
                try:
                    stock_item = MainStorage.objects.get(device_imei=item)
                    stock_item.stock_out_date = date
                    stock_item.sold = True
                    stock_item.in_stock = False
                    if sales_type == 'Loan':
                        stock_item.sales_type = sales_type
                        stock_item.pending = True
                    else:
                        stock_item.sales_type = sales_type
                        stock_item.pending = False
                        stock_item.paid = True
                    stock_item.save()
                except MainStorage.DoesNotExist:
                    not_in_stock.append(item)
            print(not_in_stock)
            return JsonResponse({'status': 200, 'not_in_stock': not_in_stock})
        else:
            return JsonResponse({'status': 400, 'error': 'No data received'})
    else:
        agents = UserProfile.objects.filter(groups__name='agents')
        agents = sorted(agents, key=lambda x: x.username)
        special_outlets = UserProfile.objects.filter(groups__name='special_sales')
        agents = list(set(agents + sorted(special_outlets, key=lambda x: x.username)))
    return render(request, 'users/admin_sites/upload_sales.html', {'agents': sorted(agents, key=lambda x: x.username)})
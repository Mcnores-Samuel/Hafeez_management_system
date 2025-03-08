#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains combined data collection view function, which is responsible
for handling the collection of customer and phone data during the phone purchasing
process by agents.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ...models.main_storage import MainStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from webpush import send_user_notification
from ...models.accessories import Accessories, Accessory_Sales
from ...models.appliances import Appliances, Appliance_Sales
from ...models.refarbished_devices import RefarbishedDevices, RefarbishedDevicesSales
from django.utils import timezone


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
    if (request.user.is_authenticated and request.user.groups.filter(name='staff_members').exists() 
        or request.user.is_staff and request.user.is_superuser):
        if request.method == 'POST':
            payment = request.POST.get('payment_method')
            item = MainStorage.objects.get(id=data_id)
            if item.in_stock and not item.sold:
                if payment == 'Cash':
                    date = request.POST.get('date')
                    price = request.POST.get('price')
                    item.in_stock = False
                    item.sold = True
                    item.pending = True
                    item.sales_type = 'Cash'
                    item.stock_out_date = date
                    item.price = price
                    messages.success(request, '{} of imei {} sold successfully'.format(
                        item.name, item.device_imei
                    ))
                    item.save()
                    payload = {'head': 'Sales Notification', 'body': '{} of imei {} sold successfully'.format(
                        item.name, item.device_imei
                    ), 'icon': 'https://raw.githubusercontent.com/Mcnores-Samuel/Hafeez_management_system/main/system_core_1/static/images/logo.png', 'url': 'www.hafeezmw.com'}
                    send_user_notification(user=request.user, payload=payload, ttl=1000)
                    return redirect('data_search')
            else:
                messages.error(request, 'Phone out of stock')
    if request.user.is_staff and request.user.is_superuser:
        return render(request, 'users/admin_sites/salespoint.html')
    if request.user.groups.filter(name='branches').exists():
        return render(request, 'users/branches/salespoint.html')
    return render(request, 'registration/salespoint.html')


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
    if request.method == 'POST' and request.user.is_staff and request.user.is_superuser\
        or request.user.groups.filter(name='branches').exists() and request.method == 'POST':
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
            return JsonResponse({'status': 200, 'not_in_stock': not_in_stock})
        else:
            return JsonResponse({'status': 400, 'error': 'No data received'})
    if request.user.groups.filter(name='branches').exists():
        return render(request, 'users/branches/upload_sales.html')
    return render(request, 'users/admin_sites/upload_sales.html')


@login_required
def accessary_sales(request):
    """
    The `Accessaries_Sales` view function is a Django view responsible for
    handling the sales of accessories by agents.

    Functionality:
    - Checks if the user is authenticated and is an agent. Only agents are allowed
      to access this view.
    - Verifies if the agent has available stock of accessories.
    - Renders the accessories sales form for agents to select accessories for sale.
    - Creates a record of the accessories sale in the database.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - If the user is not authenticated or is not an agent, it returns a 403 Forbidden
      response.
    - If the agent is authenticated and has stock, it renders the accessories sales form.

    Usage:
    Agents access this view to sell accessories.
    It ensures that agents with available stock can proceed with accessory sales.
    """
    if request.user.is_staff and request.user.is_superuser:
        if request.method == 'POST':
            accessory_name = request.POST.get('name')
            model = request.POST.get('model')
            quantity = int(request.POST.get('quantity'))
            price_sold = request.POST.get('selling_price')
            if quantity <= 0:
                messages.error(request, 'Quantity must be greater than 0, please check and try again')
                return redirect('data_search')
            try:
                item = Accessories.objects.filter(item=accessory_name, model=model).first()
                if item is None:
                    messages.error(request, 'Invalid accessory name or model, please check and try again')
                    return redirect('data_search')
                if item.total >= int(quantity):
                    item.previous_total = item.total
                    item.total -= int(quantity)
                    item.date_modified = timezone.now()
                    sales = Accessory_Sales()
                    sales.item = item
                    sales.model = model
                    sales.total = int(quantity)
                    sales.cost = item.cost_per_item
                    sales.price_sold = int(price_sold)
                    sales.profit = (int(price_sold) - item.cost_per_item) * int(quantity)
                    sales.date_sold = timezone.now()
                    sales.sold_by = request.user
                    sales.save()
                    item.save()
                    messages.success(request, 'Successfully sold {} of {}(s)'.format(quantity, item.item))
                    return redirect('data_search')
                messages.error(request, 'Insufficient stock, please check the quantity and try again')
            except Accessories.DoesNotExist:
                messages.error(request, 'Invalid accessory name or model, please check and try again')
                return redirect('data_search')
        return redirect('data_search')
    return redirect('data_search')


@login_required
def appliance_sales(request):
    """
    The `Appliance_Sales` view function is a Django view responsible for
    handling the sales of appliances by agents.

    Functionality:
    - Checks if the user is authenticated and is an agent. Only agents are allowed
      to access this view.
    - Verifies if the agent has available stock of appliances.
    - Renders the appliances sales form for agents to select appliances for sale.
    - Creates a record of the appliance sale in the database.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - If the user is not authenticated or is not an agent, it returns a 403 Forbidden
      response.
    - If the agent is authenticated and has stock, it renders the appliances sales form.

    Usage:
    Agents access this view to sell appliances.
    It ensures that agents with available stock can proceed with appliance sales.
    """
    if request.user.is_staff and request.user.is_superuser:
        if request.method == 'POST':
            appliance_name = request.POST.get('name')
            model = request.POST.get('model')
            quantity = int(request.POST.get('quantity'))
            price_sold = request.POST.get('selling_price')
            if quantity <= 0:
                messages.error(request, 'Quantity must be greater than 0, please check and try again')
                return redirect('data_search')
            try:
                item = Appliances.objects.filter(name=appliance_name, model=model).first()
                if item is None:
                    messages.error(request, 'Invalid appliance name or model, please check and try again')
                    return redirect('data_search')
                if item.total >= int(quantity):
                    item.previous_total = item.total
                    item.total -= int(quantity)
                    item.date_modified = timezone.now()
                    sales = Appliance_Sales()
                    sales.item = item
                    sales.model = model
                    sales.total = int(quantity)
                    sales.cost = item.cost
                    sales.price_sold = int(price_sold)
                    sales.profit = (int(price_sold) - item.cost) * int(quantity)
                    sales.date_sold = timezone.now()
                    sales.sold_by = request.user
                    sales.save()
                    item.save()
                    messages.success(request, 'Successfully sold {} of {}(s)'.format(quantity, item.name))
                    return redirect('data_search')
                messages.error(request, 'Insufficient stock, please check the quantity and try again')
            except Appliances.DoesNotExist:
                messages.error(request, 'Invalid appliance name or model, please check and try again')
                return redirect('data_search')
        return redirect('data_search')
    return redirect('data_search')


@login_required
def refarbished_sales(request):
    """
    The `salesRegister` view function is a Django view responsible for
    handling the sales register of agents.

    Functionality:
    - Checks if the user is authenticated and is an agent. Only agents are allowed
      to access this view.
    - Renders the sales register page for agents to view their sales records.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - If the user is not authenticated or is not an agent, it returns a 403 Forbidden
      response.
    - If the agent is authenticated, it renders the sales register page.

    Usage:
    Agents access this view to view their sales records.
    It ensures that only agents are able to access this view.
    """
    if request.user.is_staff and request.user.is_superuser:
        if request.method == 'POST':
            device_name = request.POST.get('name')
            model = request.POST.get('model')
            quantity = int(request.POST.get('quantity'))
            price_sold = request.POST.get('selling_price')
            if quantity <= 0:
                messages.error(request, 'Quantity must be greater than 0, please check and try again')
                return redirect('data_search')
            try:
                item = RefarbishedDevices.objects.filter(name=device_name, model=model).first()
                if item is None:
                    messages.error(request, 'Invalid device name or model, please check and try again')
                    return redirect('data_search')
                if item.total >= int(quantity):
                    item.previous_total = item.total
                    item.total -= int(quantity)
                    item.date_modified = timezone.now()
                    sales = RefarbishedDevicesSales()
                    sales.name = item
                    sales.model = model
                    sales.total = int(quantity)
                    sales.cost = item.cost
                    sales.price_sold = int(price_sold)
                    sales.profit = (int(price_sold) - item.cost) * int(quantity)
                    sales.date_sold = timezone.now()
                    sales.sold_by = request.user
                    sales.save()
                    item.save()
                    messages.success(request, 'Successfully sold {} of {}(s)'.format(quantity, item.name))
                    return redirect('data_search')
                messages.error(request, 'Insufficient stock, please check the quantity and try again')
            except MainStorage.DoesNotExist:
                messages.error(request, 'Invalid device name or model, please check and try again')
                return redirect('data_search')
        return redirect('data_search')
    return redirect('data_search')
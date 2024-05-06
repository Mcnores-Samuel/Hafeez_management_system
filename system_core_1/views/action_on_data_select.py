#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from ..data_query_engine.agents_queries.agents_data_query import AgentsDataQuery
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models.main_storage import MainStorage
from ..models.agent_profile import AgentProfile
from django.core.mail import send_mail
from ..models.user_profile import UserProfile


@login_required
def sale_on_cash(request):
    """The `sale_on_cash` view function is responsible for handling the sale of a
    phone on cash.
    """
    if request.method == 'POST':
        user = request.user
        if user.groups.filter(name='agents').exists():
            device_imei = request.POST.get('device_imei')
            amount = request.POST.get('amount')
            cassproof_image = request.FILES.get('cash_proof')
            agent_profile = AgentProfile.objects.get(user=user)
            admin = UserProfile.objects.filter(is_staff=True, is_superuser=True, is_active=True)
            admin_list = [admin.email for admin in admin]
            if agent_profile:
                device = MainStorage.objects.get(device_imei=device_imei)
                device.in_stock = False
                device.pending = True
                device.sold = True
                device.sales_type = 'Cash'
                device.price = amount
                device.trans_image = cassproof_image
                device.save()
                send_mail(
                    'ATTENTION: New Sale On Cash To Approve',
                    f"Hello Admin, {user.username} has made a sale on cash and is pending approval. \
                    Please login to the system to approve the sale. Device: {device.name}, \
                    Imei: {device.device_imei}, Amount: {amount} click here to approve: \
                    www.hafeezmw.com",
                    'noreply.hafeezmw@gmail.com', admin_list)
                messages.success(request, 'Your sale has been successfully processed and is pending approval.')
                return redirect('in_stock')
            messages.error(request, 'An error occurred while processing your sale. Please try again or contact the administrator.')
    return redirect('in_stock')


@login_required
def sale_on_loan(request, data_id):
    """The `sale_on_loan` view function is responsible for handling the sale of a
    phone on loan.
    """
    if request.method == 'GET':
        user = request.user
        device = AgentsDataQuery().sale_on_credit(user, data_id)
        if device:
            messages.success(request, 'Your sale has been successfully processed and is pending approval.')
            return redirect('in_stock')
        else:
            messages.error(request,
                           'An error occurred while processing your sale. Please try again or contact the administrator.')
    return redirect('in_stock')

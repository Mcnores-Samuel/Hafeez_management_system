#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from ..forms.agent_stock_form import AssignAgentForm
from ..models.main_storage import MainStorage
from ..models.agent_stock import AgentStock
from ..models.agent_profile import AgentProfile
from ..models.user_profile import UserProfile
from django.utils import timezone



def action_on_click(request, data_id):
    if request.method == 'POST':
        form = AssignAgentForm(request.POST)
        if form.is_valid():
            user = UserProfile.objects.get(username=form.cleaned_data['agent'])
            agent = AgentProfile.objects.get(user=user.id)
            phone = MainStorage.objects.get(id=data_id)
            new_stock = AgentStock(agent=agent, imei_number=phone.device_imei,
                                   phone_type=phone.phone_type,
                                   collection_date=timezone.now(),
                                   sales_type='Loan', in_stock=True, stock_out_date=timezone.now())
            new_stock.save()
            phone.assigned = True
            phone.save()
            return redirect('main_storage')
    else:
        form = AssignAgentForm()
    return render(request, 'users/admin_action.html', {'form': form})
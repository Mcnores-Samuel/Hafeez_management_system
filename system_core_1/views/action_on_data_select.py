#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from ..forms.agent_stock_form import AssignAgentForm
from ..models.main_storage import MainStorage
from ..models.user_profile import UserProfile



def deploy_device(request, data_id):
    """The `deploy_device` view function is responsible for handling the deployment
    of a phone from the main storage to an agent.
    """
    if request.user.is_staff:
        if request.method == 'POST':
            form = AssignAgentForm(request.POST)
            if form.is_valid():
                user = UserProfile.objects.get(username=form.cleaned_data['agent'])
                phone = MainStorage.objects.get(id=data_id)
                if user:
                    phone.agent = user
                phone.assigned = True
                phone.save()
                return redirect('main_storage')
        else:
            form = AssignAgentForm()
    return render(request, 'users/admin_sites/admin_action.html', {'form': form})

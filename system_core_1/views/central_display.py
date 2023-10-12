#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""This module contains the views for the application."""
from django.shortcuts import render
from ..forms import *
from ..models import AgentProfile
from django.contrib.auth.decorators import login_required
from ..models.agent_profile import AgentProfile
from ..models.user_profile import UserProfile
from ..models.main_storage import MainStorage
from ..models.agent_stock import AgentStock
from ..forms.filters import FilterMainStorege
from ..forms.search_filters import FilterMainStoregeForm
from ..forms.filters import FilterAgentAndData
from django.db.models import Q, Prefetch

@login_required
def users(request):
    """The `users` view function is responsible for handling the display of all users
    in the application.

    Functionality:
    - Checks if the user is authenticated and is a staff member. Only staff members
      are allowed to access this view.
    - Renders the users page, displaying all users in the application.
    """
    content = None
    if request.user.is_staff:
        all_users = UserProfile.objects.all().order_by('id')
        agents = AgentProfile.objects.all().order_by('id')
        content = {'users': all_users, 'agents': agents}
    return render(request, 'users/users.html', content)


@login_required
def main_storage(request):
    """The `main_storage` view function is responsible for handling the display of
    all phones in the main storage.

    Functionality:
    - Checks if the user is authenticated and is a staff member. Only staff members
      are allowed to access this view.
    - Renders the main storage page, displaying all phones in the main storage.
    - Implements search and filtering functionality.
    - Implements pagination functionality.

    Note:
    This view assumes user authentication and validation of staff status have been
    handled in the authentication system and UserProfile model.
    """
    content = None
    if request.user.is_staff:
        queryset = MainStorage.objects.all().order_by('id')
        filter = FilterMainStorege(request.GET, queryset=queryset)
        search_filter = FilterMainStoregeForm(request.GET)
        if filter.is_valid():
            queryset = filter.qs
        
        if search_filter.is_valid():
            search_query = search_filter.cleaned_data.get('search_query')

            if search_query:
                queryset = queryset.filter(
                    Q(phone_type__icontains=search_query) |
                    Q(device_imei__icontains=search_query) |
                    Q(contract_no__icontains=search_query)
                )

        content = {'data': queryset, 'filter': filter, 'search_filter': search_filter}
    return render(request, 'users/main_stock.html', content)


def agents_and_data(request):
    """The `agents_and_data` view function is responsible for handling the display of
    all agents and their phone data.
    """
    data_by_agent = []

    if request.user.is_staff:
        filter = FilterAgentAndData(request.GET, queryset=AgentProfile.objects.all().order_by('id'))
        if filter.is_valid():
            agents = filter.qs
        else:
            agents = AgentProfile.objects.all().order_by('id').prefetch_related(
                Prefetch('agentstock_set', queryset=AgentStock.objects.all().order_by('id'))
            )

        data_by_agent = [(agent, list(agent.agentstock_set.all())) for agent in agents]

    return render(request, 'users/admin_agent_view.html', {'data_by_agent': data_by_agent, 'filter': filter})

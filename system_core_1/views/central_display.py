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
from ..models.customer_details import CustomerData
from ..forms.filters import FilterMainStorege
from ..forms.search_filters import FilterMainStoregeForm
from ..forms.filters import FilterAgentAndData
from django.db.models import Q
from ..models.user_profile import UserAvatar

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
        user = request.user
        all_users = UserProfile.objects.all().order_by('id')
        agents = AgentProfile.objects.all().order_by('id')
        avatar = UserAvatar.objects.get(user=request.user)
        content = {'users': all_users,
                   'agents': agents,
                   'profile': user.email[0],
                   'avatar': avatar}
    return render(request, 'users/admin_sites/users.html', content)


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
        user = request.user
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
                    Q(contract_no__icontains=search_query) |
                    Q(sales_type__icontains=search_query) |
                    Q(entry_date__icontains=search_query) |
                    Q(stock_out_date__icontains=search_query) |
                    Q(agent__username__icontains=search_query) |
                    Q(category__icontains=search_query)
                )
        avatar = UserAvatar.objects.get(user=request.user)
        content = {'data': queryset,
                   'filter': filter,
                   'search_filter': search_filter,
                   'profile': user.email[0],
                   'avatar': avatar}
    return render(request, 'users/admin_sites/main_stock.html', content)


def agents_and_data(request):
    """The `agents_and_data` view function is responsible for handling the display of
    all agents and their phone data.
    """
    data_by_agent = {}
    content = None

    if request.user.is_staff:
        user = request.user
        queryset = MainStorage.objects.all().order_by('id')
        agents = AgentProfile.objects.all().order_by('id')
        filter = FilterAgentAndData(request.GET, queryset=AgentProfile.objects.all().order_by('id'))
        if filter.is_valid():
            agents = filter.qs
        for agent in agents:
            data_by_agent[agent] = list(queryset.filter(agent=agent.user.id, in_stock=True))
        avatar = UserAvatar.objects.get(user=request.user)
        content = {
                   'data_by_agent': data_by_agent,
                   'filter': filter,
                   'profile': user.email[0],
                     'avatar': avatar}
    return render(request, 'users/admin_sites/admin_agent_view.html', content)



def my_customers(request):
    """The `my_customers` view function is responsible for handling the display of
    all customers and their phone data.

    Functionality:
    - Checks if the user is authenticated and is an agent. Only agents are allowed
      to access this view.
    - Renders the my customers page, displaying all customers and their phone data.
    - Implements pagination functionality.

    Note:
    This view assumes user authentication and validation of agent status have been
    handled in the authentication system and AgentProfile model.
    """
    data_by_customer = []
    user = request.user
    if user.groups.filter(name='agents').exists():
        print("User ID:", user.id)
        customer_data = CustomerData.objects.filter(agent=user.id).order_by('id')
        print("Customer Data:", customer_data)
        data_by_customer = [(customer, list(customer.phonedata_set.all())) for customer in customer_data]
    print(data_by_customer)
    return render(request, 'users/agent_sites/my_customers.html', {'data_by_customer': data_by_customer,
                                                               'profile': user.email[0]})
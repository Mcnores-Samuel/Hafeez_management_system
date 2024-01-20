#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the views for the search and filters functionality.

The search and filters functionality is implemented using the django-filter package.
and will be used to filter and search for phones in the main storage and agent stock.

The search and filters will be handled as a restful API and will be accessed using
the following URLs:
- /system_core_1/main_storage/search_and_filters
- /system_core_1/agent_stock/search_and_filters
where system_core_1 is the name of the Django application.
all data is returned in JSON format.
"""
from ..models.main_storage import MainStorage
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models.customer_details import CustomerData


@login_required
def data_search(request):
    """The `data_search` view function is responsible for handling the search
    functionality for all data in the application.

    Functionality:
    - Checks if the user is authenticated and is a staff member. Only staff members
      are allowed to access this view.
    - Implements search functionality for all data in the application.
    - Returns a JSON response containing the search results.

    Note:
    This view assumes user authentication and validation of staff status have been
    handled in the authentication system and UserProfile model.
    """
    if request.method == 'POST':
        search_query = request.POST.get('search_query', None)
        queryset = []
        if search_query:
            queryset = MainStorage.objects.all()
            queryset = queryset.filter(
                    Q(device_imei__icontains=search_query) |
                    Q(contract_no__icontains=search_query)
                )
    return render(request, 'users/staff_sites/search.html', {'data': queryset})


def search(search_query):
    """The `search` view function is responsible for handling the search
    functionality for all data in the application.
    """
    queryset = MainStorage.objects.all()
    if search_query:
        queryset = queryset.filter(
            Q(phone_type__iexact=search_query) |
            Q(device_imei__icontains=search_query) |
            Q(contract_no__icontains=search_query) |
            Q(sales_type__icontains=search_query) |
            Q(entry_date__icontains=search_query) |
            Q(stock_out_date__icontains=search_query) |
            Q(agent__username__icontains=search_query) |
            Q(category__icontains=search_query)
        )
    return queryset

def search_customers(request):
    """The `search_customers` view function is responsible for handling the search
    functionality for all data in the application.
    """
    if request.method == 'POST':
        search_query = request.POST.get('search_query', None)
        queryset = []
        if search_query:
            queryset = CustomerData.objects.all()
            queryset = queryset.filter(
                    Q(agent__user__username__icontains=search_query) |
                    Q(customer_name__icontains=search_query) |
                    Q(national_id__icontains=search_query) |
                    Q(customer_contact__icontains=search_query) |
                    Q(second_contact__icontains=search_query) |
                    Q(first_witness_name__icontains=search_query) |
                    Q(first_witness_contact__icontains=search_query) |
                    Q(account_name__icontains=search_query)
                ).order_by('-created_at')
        customers = [(customer, list(customer.phonedata_set.all())) for customer in queryset]

        context = {
            'customers': customers
        }
        return render(request, 'users/staff_sites/search_customers.html', context)
    return render(request, 'users/staff_sites/search_customers.html')

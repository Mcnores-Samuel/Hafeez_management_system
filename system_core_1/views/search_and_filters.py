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
from django.views.decorators.csrf import csrf_exempt
from ..models.user_profile import UserProfile
from ..models.accessories import Accessories
from ..models.appliances import Appliances


@login_required
@csrf_exempt
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
    queryset = []

    data_list_ac = Accessories.objects.all()
    name_set_ac = set()
    model_set_ac = set()
    for data in data_list_ac:
        name_set_ac.add(data.item)
        model_set_ac.add(data.model)
    sorted_name_list_ac = sorted(list(name_set_ac))
    sorted_model_list_ac = sorted(list(model_set_ac))
    
    data_list_ap = Appliances.objects.all()
    name_set_ap = set()
    model_set_ap = set()
    for data in data_list_ap:
        name_set_ap.add(data.name)
        model_set_ap.add(data.model)
    sorted_name_list_ap = sorted(list(name_set_ap))
    sorted_model_list_ap = sorted(list(model_set_ap))
    
    if request.method == 'POST':
        search_query = request.POST.get('search_query', None)
        queryset = []
        if search_query:
            queryset = MainStorage.objects.all()
            queryset = queryset.filter(
                    Q(device_imei__icontains=search_query) |
                    Q(device_imei_2__icontains=search_query) |
                    Q(contract_no__icontains=search_query)
                )
    if request.user.is_staff and request.user.is_superuser:
        return render(request, 'users/admin_sites/search.html',
                      {'data': queryset, 'names_ac': sorted_name_list_ac, 'models_ac': sorted_model_list_ac,
                       'names_ap': sorted_name_list_ap, 'models_ap': sorted_model_list_ap})


@login_required
@csrf_exempt
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

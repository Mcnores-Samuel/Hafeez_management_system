#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from ..data_query_engine.agents_queries.agents_data_query import AgentsDataQuery
from django.contrib import messages


def sale_on_cash(request, data_id):
    """The `sale_on_cash` view function is responsible for handling the sale of a
    phone on cash.
    """
    if request.method == 'GET':
        user = request.user
        device = AgentsDataQuery().sale_on_cash(user, data_id)
        messages.success(request, 'Please confirm by providing transaction details including imei number through proper channels.')
        if device:
            return redirect('in_stock')
    return redirect('in_stock')


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

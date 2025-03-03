"""This module contains the agents data access view functions, which are the main entry points,
for agents to access and interact with the application's data.

The agents data access views provide agents with access to the application's data, allowing them
to view, search, and manage stock data, sales data, and other relevant information.
"""
from ...data_query_engine.agents_queries.agents_data_query import AgentsDataQuery
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def my_pending_sales(request):
    """Display the pending sales data.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
        Returns a list of pending sales to be resolved.
    """
    user = request.user
    pendingSales, total = AgentsDataQuery().pending_sales(user, request)
    if pendingSales:
        context = {
            'pending_sales': pendingSales,
            'page_total': len(pendingSales),
            'total': total
        }
        return render(request, 'users/agent_sites/pending_sales.html', context)
    messages.error(request, 'An error occurred while fetching pending sales data.')
    return render(request, 'users/agent_sites/pending_sales.html')


@login_required
def issues(request):
    """Display the issues data.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
        Returns a list of issues to be resolved.
    """
    user = request.user
    issues = AgentsDataQuery().agent_issues(user, request)
    if issues:
        context = {
            'issues': issues
        }
        messages.warning(request, "Please follow up on the issues below. Thank you.")
        return render(request, 'users/agent_sites/issues.html', context)
    messages.info(request, 'There are no issues to display. Please check back later.')
    return render(request, 'users/agent_sites/issues.html')


@login_required
def faulty_devices(request):
    """Display the faulty devices data.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
        Returns a list of faulty devices.
    """
    user = request.user
    faultyDevices = AgentsDataQuery().agent_faults(user, request)
    if faultyDevices:
        context = {
            'faulty_devices': faultyDevices
        }
        return render(request, 'users/agent_sites/faulty_devices.html', context)
    messages.info(request, 'There are no faulty devices to display. Please check back later.')
    return render(request, 'users/agent_sites/faulty_devices.html')


@login_required
def new_stock(request):
    """Display the new stock data.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
        Returns a list of new stock.
    """
    user = request.user
    newStock = AgentsDataQuery().agent_new_stock(user, request)
    if newStock:
        context = {
            'new_stock': newStock
        }
        return render(request, 'users/agent_sites/new_stock.html', context)
    messages.info(request, 'There is no new stock to display. Please check back later.')
    return render(request, 'users/agent_sites/new_stock.html')

"""This module contains the views for the revenues app.

The revenues app is responsible for handling the revenue data of the system.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ...models.main_storage import MainStorage
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum


@login_required
def accounting(request):
    """Display the revenues page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    return render(request, 'users/admin_sites/accounting.html')


@login_required
def cost_and_expenses(request):
    """Display the cost and expenses page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    return render(request, 'users/admin_sites/cost_and_expenses.html')
    
    

@login_required
def getCostAndRevenue(request):
    """Returns a JSON object containing the total cost and revenue."""
    if request.method == 'GET':
        this_month = timezone.now().month
        total_cost = MainStorage.objects.filter(
            in_stock=False, sold=True, pending=False, cost__gt=0, price__gt=0,
            stock_out_date__month=this_month, stock_out_date__year=timezone.now().year,
            assigned=True, agent__groups__name='agents').aggregate(
            total_cost=Sum('cost'))
        total_revenue = MainStorage.objects.filter(
            in_stock=False, sold=True, pending=False, assigned=True,
            stock_out_date__month=this_month, cost__gt=0, price__gt=0,
            stock_out_date__year=timezone.now().year, agent__groups__name='agents').aggregate(
            total_revenue=Sum('price'))
        return JsonResponse({
            'total_cost': total_cost['total_cost'],
            'total_revenue': total_revenue['total_revenue']
        })
    return JsonResponse({'error': 'Invalid request.'})

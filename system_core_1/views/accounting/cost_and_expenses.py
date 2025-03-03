"""This module contains the cost and expenses view."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from system_core_1.models.main_storage import MainStorage
from django.db.models import Sum

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
def availableStockCost(request):
    """Returns the total cost of available stock."""
    if request.method == 'GET':
        total_cost = MainStorage.total_cost()
        return JsonResponse({'total_cost': total_cost})
    return JsonResponse({'error': 'Invalid request.'})
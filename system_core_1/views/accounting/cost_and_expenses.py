"""This module contains the cost and expenses view."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from system_core_1.models.main_storage import MainStorage
from system_core_1.models.refarbished_devices import RefarbishedDevices
from system_core_1.models.appliances import Appliances
from system_core_1.models.accessories import Accessories
from system_core_1.models.user_profile import UserProfile


@login_required
def cost_and_expenses(request):
    """Display the cost and expenses page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    agents = UserProfile.objects.filter(groups__name='agents').values_list(
        'username', flat=True)
    partners = UserProfile.objects.filter(groups__name='partners').values_list(
        'username', flat=True)
    staff = UserProfile.objects.filter(groups__name='staff_members').values_list(
        'username', flat=True)
    admin = UserProfile.objects.filter(is_superuser=True).values_list(
        'username', flat=True)
    expense_holder = UserProfile.objects.filter(groups__name='expense_holders').values_list(
        'username', flat=True)
    users = sorted(agents.union(partners, staff, admin, expense_holder))
    return render(request, 'users/admin_sites/cost_and_expenses.html', {'users': users})


@login_required
def availableStockCost(request):
    """Returns the total cost of available stock."""
    if request.method == 'GET':
        total_cost = MainStorage.total_cost()
        total_refarbished_cost = RefarbishedDevices.total_cost()
        total_appliance_cost = Appliances.total_cost()
        total_accessory_cost = Accessories.total_cost()
        
        if total_refarbished_cost is not None:
            total_cost += total_refarbished_cost
        
        if total_appliance_cost is not None:
            total_cost += total_appliance_cost

        if total_accessory_cost is not None:
            total_cost += total_accessory_cost
        
        return JsonResponse({'total_cost': total_cost})
    return JsonResponse({'error': 'Invalid request.'})
"""This module contains the JSON response for the total assets."""
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from system_core_1.models.expenses import FixedAssets
from system_core_1.models.main_storage import MainStorage
from system_core_1.models.refarbished_devices import RefarbishedDevices
from system_core_1.models.appliances import Appliances
from system_core_1.models.accessories import Accessories
from django.shortcuts import redirect
from django.contrib import messages


@login_required
def add_assets(request):
    """This function adds an asset."""
    if request.method == 'POST' and request.user.is_superuser:
        asset_name = request.POST.get('assetName')
        description = request.POST.get('assetDescription')
        useful_life = request.POST.get('assetLife')
        cost = request.POST.get('assetCost')
        date_purchased = request.POST.get('assetDate')

        FixedAssets.objects.create(
            name=asset_name,
            description=description,
            useful_life=useful_life,
            cost=cost,
            date_purchased=date_purchased,
            salvage_value=0,
            depreciation=0
        )
        messages.success(request, 'Asset added successfully.')
        return redirect('cost_and_expenses')
    messages.error(request, 'Error adding asset.')
    return redirect('cost_and_expenses')


@login_required
def total_assets(request):
    """This function returns the total assets."""
    if request.method == 'GET' and request.user.is_superuser:
        total_assets = MainStorage.total_cost() + RefarbishedDevices.total_cost() +\
            Appliances.total_cost() + Accessories.total_cost() + FixedAssets.total_assets_cost()
        return JsonResponse({'total_assets': total_assets})
    return JsonResponse({'error': 'Invalid request.'})
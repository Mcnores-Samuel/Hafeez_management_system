"""This module contains the JSON response for the total assets."""
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from system_core_1.models.expenses import FixedAssets
from system_core_1.models.main_storage import MainStorage
from system_core_1.models.refarbished_devices import RefarbishedDevices
from system_core_1.models.appliances import Appliances
from system_core_1.models.accessories import Accessories


@login_required
def total_assets(request):
    """This function returns the total assets."""
    if request.method == 'GET' and request.user.is_superuser:
        total_assets = MainStorage.total_cost() + RefarbishedDevices.total_cost() +\
            Appliances.total_cost() + Accessories.total_cost() + FixedAssets.total_assets_cost()
        return JsonResponse({'total_assets': total_assets})
    return JsonResponse({'error': 'Invalid request.'})
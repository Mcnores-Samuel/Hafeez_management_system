from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from system_core_1.models.main_storage import Airtel_mifi_storage
import json


@login_required
@csrf_exempt
def add_airtel_devices_stock(request):
    """This view function is responsible for handling the addition of Airtel MiFi devices to stock.

    Functionality:
    - Checks if the user is authenticated and is an agent. Only agents are allowed
      to access this view.
    - Renders the add Airtel MiFi devices to stock form.
    - If the form is submitted, the Airtel MiFi device is added to stock.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - If the user is not authenticated or is not an agent, it returns a 403 Forbidden
      response.
    - If the agent is authenticated and has stock, it renders the add Airtel MiFi devices
      to stock form.

    Usage:
    Agents access this view to add Airtel MiFi devices to stock.
    It ensures that only agents are able to access this view.
    """
    if (request.user.is_authenticated and request.user.groups.filter(name='airtel').exists()
        or request.user.is_staff and request.user.is_superuser):
        if request.method == 'POST':
            data = json.loads(request.POST.get('data'))
            device_type = request.POST.get('device_type')
            already_exists = []
            for item in data:
              try:
                  Airtel_mifi_storage.objects.create(
                      device_imei=item, device_type=device_type, in_stock=True,
                      entry_date=timezone.now(), last_updated=timezone.now(),
                      updated_by=request.user.username, days_left=0
                  )
              except Exception as e:
                already_exists.append(item)
            return JsonResponse({'status': 200, 'data': already_exists})
        return render(request, 'users/airtel_sites/add_to_stock.html')
    return redirect('dashboard')

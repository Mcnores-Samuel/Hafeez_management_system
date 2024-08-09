from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from ..models.main_storage import Airtel_mifi_storage
from django.db.models import Q
from django.contrib import messages


@login_required
def search_airtel_devices(request):
    """This view function is responsible for searching for Airtel devices.

    Functionality:
    - Checks if the user is authenticated and is a staff member. Only staff members are allowed
      to access this view.
    - Renders the search Airtel devices form.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - If the user is not authenticated or is not a staff member, it returns a 403 Forbidden
      response.
    - If the staff member is authenticated, it renders the search Airtel devices form.

    Usage:
    Staff members access this view to search for Airtel devices.
    It ensures that only staff members are able to access this view.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='airtel').exists():
        devices = Airtel_mifi_storage.objects.filter(
            in_stock=True)
        if request.method == 'POST':
            search_query = request.POST.get('search_query')
            device = Airtel_mifi_storage.objects.filter(
                Q(device_imei__icontains=search_query)
            )
            return render(request, 'users/airtel_sites/search_airtel_devices.html', {'devices': device})
        messages.warning(request, 'Please enter a search query')
        return render(request, 'users/airtel_sites/search_airtel_devices.html',
                      {'devices': devices})
    return HttpResponseForbidden()
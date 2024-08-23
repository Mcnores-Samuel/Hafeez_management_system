from ..models.main_storage import Airtel_mifi_storage
from ..models.user_profile import UserProfile
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse


@login_required
def return_device(request):
    """This view function is responsible for returning an Airtel device.

    Functionality:
    - Checks if the user is authenticated and is a staff member. Only staff members are allowed
      to access this view.
    - Renders the return device form.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - If the user is not authenticated or is not a staff member, it returns a 403 Forbidden
      response.
    - If the staff member is authenticated, it renders the return device form.

    Usage:
    Staff members access this view to return an Airtel device.
    It ensures that only staff members are able to access this view.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='airtel').exists():
        if request.method == 'POST':
            device_id = request.POST.get('device_id')
            prom_id = request.POST.get('promoter_id')
            device = Airtel_mifi_storage.objects.get(id=device_id)
            promoter = UserProfile.objects.get(id=prom_id)
            if device:
                device.in_stock = True
                device.promoter = None
                device.team_leader = None
                device.last_updated = timezone.now()
                device.returned = True
                device.days_left = 0
                device.device_phone_no = None
                device.returned_on = timezone.now()
                device.returned_by = promoter.first_name + ' ' + promoter.last_name
                device.updated_by = request.user.first_name + ' ' + request.user.last_name
                device.save()
                messages.success(request, 'Device returned successfully')
            url = reverse('devices_per_promoter', kwargs={'promoter_id': promoter.id})
        return redirect(url)
    return redirect('search_airtel_devices')


@login_required
def sale_device(request):
    """This view function is responsible for selling an Airtel device.

    Functionality:
    - Checks if the user is authenticated and is a staff member. Only staff members are allowed
      to access this view.
    - Renders the sale device form.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - If the user is not authenticated or is not a staff member, it returns a 403 Forbidden
      response.
    - If the staff member is authenticated, it renders the sale device form.

    Usage:
    Staff members access this view to sell an Airtel device.
    It ensures that only staff members are able to access this view.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='airtel').exists():
        if request.method == 'POST':
            device_id = request.POST.get('device_id')
            prom_id = request.POST.get('promoter_id')
            device = Airtel_mifi_storage.objects.get(id=device_id)
            promoter = UserProfile.objects.get(id=prom_id)
            if device:
                device.in_stock = False
                device.last_updated = timezone.now()
                device.sale_date = timezone.now()
                device.device_phone_no = promoter.phone_number
                device.updated_by = request.user.first_name + ' ' + request.user.last_name
                device.save()
                messages.success(request, 'Device sold successfully')
            url = reverse('devices_per_promoter', kwargs={'promoter_id': promoter.id})
        return redirect(url)
    return redirect('search_airtel_devices')


@login_required
def edit_device(request):
    """This view function is responsible for editing an Airtel device.

    Functionality:
    - Checks if the user is authenticated and is a staff member. Only staff members are allowed
      to access this view.
    - Renders the edit device form.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - If the user is not authenticated or is not a staff member, it returns a 403 Forbidden
      response.
    - If the staff member is authenticated, it renders the edit device form.

    Usage:
    Staff members access this view to edit an Airtel device.
    It ensures that only staff members are able to access this view.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='airtel').exists():
        if request.method == 'POST':
            device_id = request.POST.get('device_id')
            device = Airtel_mifi_storage.objects.get(id=device_id)
            if device:
                device.device_imei = request.POST.get('device_imei')
                device.device_phone_no = request.POST.get('device_phone_no')
                device.last_updated = timezone.now()
                device.updated_by = request.user.first_name + ' ' + request.user.last_name
                device.save()
                messages.success(request, 'Device edited successfully')
            url = reverse('search_airtel_devices')
        return redirect(url)
    return redirect('search_airtel_devices')
    


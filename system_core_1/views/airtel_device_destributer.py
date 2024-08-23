from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from ..models.main_storage import Airtel_mifi_storage
from ..models.user_profile import UserProfile
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.utils import timezone


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
            in_stock=True, promoter=None).all().order_by('-entry_date')
        promoters = UserProfile.objects.filter(groups__name='promoters')
        if request.method == 'POST':
            search_query = request.POST.get('search_query')
            device = Airtel_mifi_storage.objects.filter(
                Q(device_imei__icontains=search_query)
            )
            return render(request, 'users/airtel_sites/search_airtel_devices.html',
                          {'devices': device, 'promoters': promoters})
        paginator = Paginator(devices, 15)
        page = request.GET.get('page')
        try:
            devices = paginator.page(page)
        except PageNotAnInteger:
            devices = paginator.page(1)
        except EmptyPage:
            devices = paginator.page(paginator.num_pages)
        return render(request, 'users/airtel_sites/search_airtel_devices.html',
                      {'devices': devices, 'promoters': promoters})
    return HttpResponseForbidden()


@login_required
def assignPromoter(request):
    """This view function is responsible for assigning a promoter to an Airtel device.

    Functionality:
    - Checks if the user is authenticated and is a staff member. Only staff members are allowed
      to access this view.
    - Assigns a promoter to an Airtel device.
    - Checks if the device is already assigned to a promoter.
    - Checks if the device is already assigned to the same promoter.
    - Checks if the device is already assigned to another promoter.
    - Checks if the device is already assigned to a promoter and is not in stock.
    - Checks if the device is not in stock.
    - Checks if the device is not assigned to a promoter.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - If the user is not authenticated or is not a staff member, it returns a 403 Forbidden
      response.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='airtel').exists():
        if request.method == 'POST':
            device_imei = request.POST.get('device_imei')
            promoter = request.POST.get('promoter')
            device_phone_number = request.POST.get('device_phone_number')
            promoter = " ".join(promoter.split())
            prom_first_name, prom_last_name = promoter.split(' ')
            prom = UserProfile.objects.get(
                Q(first_name__icontains=prom_first_name) & Q(last_name__icontains=prom_last_name))
            team_leader = UserProfile.objects.get(id=prom.team_leader)
            device = Airtel_mifi_storage.objects.get(device_imei=device_imei)
            if device:
                try:
                    date_after_14_days = timezone.now() + timezone.timedelta(days=13)
                    device.promoter = prom
                    device.device_phone_no = device_phone_number
                    device.in_stock = True
                    device.team_leader = team_leader.first_name + ' ' + team_leader.last_name
                    device.days_left = 14
                    device.days_after_due = 0
                    device.collected_on = timezone.now()
                    device.last_updated = timezone.now()
                    device.next_due_date = date_after_14_days
                    device.updated_by = request.user.first_name + ' ' + request.user.last_name
                    device.save()
                    messages.success(request, 'You have successfully assigned {} to {}'.format(
                        device.device_imei, promoter))
                except Exception as e:
                    if 'device_phone_no' in str(e) and 'unique' in str(e):
                        messages.error(request, 'The device phone number is already assigned to another device')
                    else:
                        messages.error(request, 'something went wrong while assigning the device')
                    return redirect('search_airtel_devices')
            else:
                messages.error(request, 'The device is not in stock or is not available')
            return redirect('search_airtel_devices')
    messages.error(request, 'You are not authorized to access this page')
    return redirect('sign_out')
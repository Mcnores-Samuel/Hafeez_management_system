"""This view function is responsible for assigning a promoter to an Airtel device."""
from ..models.user_profile import UserProfile
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from ..models.main_storage import Airtel_mifi_storage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def promoters_data(request):
    """This view function is responsible for displaying the data of the promoters.

    Functionality:
    - Checks if the user is authenticated and is a staff member. Only staff members are allowed
      to access this view.
    - Renders the promoters data.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - If the user is not authenticated or is not a staff member, it returns a 403 Forbidden
      response.
    - If the staff member is authenticated, it renders the promoters data.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='airtel').exists():
        promoters = UserProfile.objects.filter(groups__name='promoters').all().order_by('first_name')
        data_by_promoters = []
        promoters_data = {}
        for promoter in promoters:
            promoters_data['promoter'] = promoter
            promoters_data['within_due_date'] = Airtel_mifi_storage.objects.filter(
                promoter=promoter, in_stock=True, payment_confirmed=False, paid=False,
                activated=False, next_due_date__gt=timezone.now()).count()
            promoters_data['missed_due_date'] = Airtel_mifi_storage.objects.filter(
                promoter=promoter, in_stock=True, payment_confirmed=False, paid=False,
                activated=False, next_due_date__lte=timezone.now()).count()
            if promoters_data['missed_due_date'] > 0:
                promoters_data['color_code'] = 'bg-danger'
            else:
                promoters_data['color_code'] = 'bg-success'
            promoters_data['in_danger_zone'] = True if promoters_data['missed_due_date'] > 0 else False
            promoters_data['total_devices'] = Airtel_mifi_storage.objects.filter(
                promoter=promoter, in_stock=True).count()
            data_by_promoters.append(promoters_data)
            promoters_data = {}

        paginator = Paginator(data_by_promoters, 12)
        page = request.GET.get('page')
        try:
            data_by_promoters = paginator.page(page)
        except PageNotAnInteger:
            data_by_promoters = paginator.page(1)
        except EmptyPage:
            data_by_promoters = paginator.page(paginator.num_pages)
        return render(request, 'users/airtel_sites/promoters_data.html', {'data_by_promoters': data_by_promoters})
    return HttpResponseForbidden()


@login_required
def devices_per_promoter(request, promoter_id):
    """This view function is responsible for displaying the devices per promoter.

    Functionality:
    - Checks if the user is authenticated and is a staff member. Only staff members are allowed
      to access this view.
    - Renders the devices per promoter data.

    Parameters:
    - request: The HTTP request object containing user information.
    - fullname: The full name of the promoter.

    Returns:
    - If the user is not authenticated or is not a staff member, it returns a 403 Forbidden
      response.
    - If the staff member is authenticated, it renders the devices per promoter data.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='airtel').exists():
        promoter = UserProfile.objects.get(id=promoter_id)
        total_overdue = 0
        devices = Airtel_mifi_storage.objects.filter(
            promoter=promoter, in_stock=True, payment_confirmed=False, paid=False,
            activated=False).all().order_by('next_due_date')
        for device in devices:
            if device.next_due_date.date() > timezone.now().date():
                device.days_left = (device.next_due_date.date() - timezone.now().date()).days + 1
            elif device.next_due_date > timezone.now():
                device.days_after_due = (timezone.now() - device.next_due_date).days
                device.days_left = 0
                total_overdue += 1
            device.save()

        if request.method == 'POST':
            overdue_devices = Airtel_mifi_storage.objects.filter(
                promoter=promoter, in_stock=True, payment_confirmed=False, paid=False,
                activated=False, next_due_date__lte=timezone.now()).all().order_by('next_due_date')
            return render(request, 'users/airtel_sites/devices_per_promoter.html',
                            {'overdue_devices': overdue_devices, 'promoter': promoter})
        on_time_devices = Airtel_mifi_storage.objects.filter(
            promoter=promoter, in_stock=True, payment_confirmed=False, paid=False,
            activated=False, next_due_date__gt=timezone.now()).all().order_by('next_due_date')
        paginator = Paginator(on_time_devices, 9)
        page = request.GET.get('page')
        try:
            on_time_devices = paginator.page(page)
        except PageNotAnInteger:
            on_time_devices = paginator.page(1)
        except EmptyPage:
            on_time_devices = paginator.page(paginator.num_pages)
        return render(request, 'users/airtel_sites/devices_per_promoter.html',
                      {'on_time_devices': on_time_devices, 'overdue_devices': total_overdue, 'promoter': promoter})
    return HttpResponseForbidden()
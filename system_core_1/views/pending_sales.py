"""This module contains the views related to the pending sales."""
from ..data_analysis_engine.admin_panel.mainstorage_analysis import MainStorageAnalysis
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models.main_storage import MainStorage
from ..models.user_profile import UserProfile
from django.contrib import messages as message
from django.http import JsonResponse
from webpush import send_user_notification
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse


@login_required
def pending_sales(request):
    """Display the pending sales page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == 'POST':
        device = request.POST.get('device_imei', None)
        if device:
            approved = MainStorage.objects.filter(
                device_imei=device, pending=True, missing=False)
            agent = UserProfile.objects.get(username=approved[0].agent)
            name = approved[0].name
            payload = {
                'head': '{} your sale has been approved.'.format(agent.username),
                'body': 'The sale of {} imei number {} has been approved.'.format(
                    name, device),
                'icon': 'https://raw.githubusercontent.com/Mcnores-Samuel/Hafeez_management_system/main/system_core_1/static/images/logo.png',
                'url': 'www.hafeezmw.com'
            }
            if approved:
                if (approved[0].sales_type == 'Loan'
                    and approved[0].contract_no != '##'):
                    name = approved[0].name
                    approved.update(pending=False)
                    message.success(request, '{} of {} The sale has been approved.'.format(
                        name, device))
                    send_user_notification(user=agent, payload=payload, ttl=1000)
                    url = reverse('pending_sales_details', args=[agent.username])
                    return redirect(url)
                elif (approved[0].sales_type == 'Cash'):
                    name = approved[0].name
                    approved.update(pending=False)
                    message.success(request, '{} of {} The sale has been approved.'.format(
                        name, device))
                    send_user_notification(user=agent, payload=payload, ttl=1000)
                    url = reverse('pending_sales_details', args=[agent.username])
                    return redirect(url)
                else:
                    message.warning(request, 'Please update the Contract Number to approve the sale.')
                return redirect('pending_sales')
    if request.user.is_staff and  request.user.is_superuser:
        analysis = MainStorageAnalysis()
        all_agents, total = analysis.pending_sales(request=request)
        return render(request, 'users/admin_sites/pending_sales.html',
                      {'all_agents': all_agents, 'total': total})
    

def total_pending_sales(request):
    """Returns the total pending sales.

    Returns:
        int: The total pending sales.
    """
    if request.method == 'GET':
        total = 0
        if request.user.is_staff and request.user.is_superuser:
            total = MainStorage.objects.filter(
                pending=True, sold=True, in_stock=False,
                missing=False, issue=False, faulty=False).count()
        elif request.user.groups.filter(name='agents').exists():
            total = MainStorage.objects.filter(
                pending=True, sold=True, in_stock=False,
                missing=False, issue=False, faulty=False,
                agent=request.user).count()
        if total > 0:
            admin = UserProfile.objects.filter(is_superuser=True)
            for user in admin:
                payload = {
                    'head': 'Approval Reminder',
                    'body': 'Hello {}!, There are {} pending your approval'.format(
                        user.username, total),
                    'icon': 'https://raw.githubusercontent.com/Mcnores-Samuel/Hafeez_management_system/main/system_core_1/static/images/logo.png',
                    'url': 'www.hafeezmw.com'
                }
                send_user_notification(user=user, payload=payload, ttl=1000)
    return JsonResponse({'total': total})


@login_required
def revert_to_stock(request):
    """Revert a device to stock. This function is only accessible to superusers.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.user.is_superuser:
        if request.method == 'POST':
            imei_number = request.POST.get('device_imei', None)
            if imei_number:
                main_storage = MainStorage.objects.get(device_imei=imei_number)
                if main_storage:
                    main_storage.in_stock = True
                    main_storage.sold = False
                    main_storage.pending = False
                    main_storage.stock_out_date = main_storage.entry_date
                    main_storage.sales_type = '##'
                    main_storage.contract_no = '##'
                    if main_storage.trans_image:
                        main_storage.trans_image.delete()
                    main_storage.save()
                    message.success(request, 'device reverted to stock successfully')
                return redirect('pending_sales')
    return redirect('dashboard')


@login_required
def pending_sales_details(request, username):
    """Display the details of pending sales for a specific agent.

    Args:
        request (HttpRequest): The request object.
        username (str): The username of the agent.

    Returns:
        HttpResponse: The response object.
    """
    if request.user.is_staff and request.user.is_superuser:
        total = 0
        agent = UserProfile.objects.get(username=str(username))
        sales = MainStorage.objects.filter(
            agent=agent, pending=True, sold=True, in_stock=False,
            missing=False, issue=False, faulty=False,
            recieved=True).order_by('-stock_out_date')
        total = sales.count()
        paginator = Paginator(sales, 12)

        page = request.GET.get('page')
        try:
            sales = paginator.page(page)
        except PageNotAnInteger:
            sales = paginator.page(1)
        except EmptyPage:
            sales = paginator.page(paginator.num_pages)

        return render(request, 'users/admin_sites/pending_sales_details.html',
                      {'total': total, 'sales': sales})
    return redirect('dashboard')
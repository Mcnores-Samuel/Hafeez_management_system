"""This module contains the views for handling deposit payments."""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as message
from ..models.main_storage import MainStorage
from ..models.account_manager import AccountManager
from ..models.user_profile import UserProfile
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from webpush import send_user_notification


@login_required
def pending_deposit_payments(request):
    """Display the pending deposit payments page."""
    if request.method == 'GET' and request.user.is_superuser:
        monday = timezone.now().date() - timezone.timedelta(days=timezone.now().date().weekday())
        sunday = monday + timezone.timedelta(days=6)
        data = MainStorage.objects.filter(
            stock_out_date__range=[monday, sunday], mbo_approved=True,
            in_stock=False, sold=True, recieved=True, pending=True,
            deposit_paid=False, is_locked=True, sales_type='Loan').order_by('-stock_out_date')
        total = data.count()
        data = Paginator(data, 12)
        page = request.GET.get('page')

        try:
            data = data.get_page(page)
        except PageNotAnInteger:
            data = data.page(1)
        except EmptyPage:
            data = data.page(data.num_pages)

        
        return render(request, 'users/admin_sites/pending_deposit_payments.html',
                      {'pending_sales': data, 'total': total})
    if request.user.is_staff and request.user.is_superuser:
        return render(request, 'users/admin_sites/pending_deposit_payments.html')
    return redirect('dashboard')


@login_required
def process_deposit_payment(request):
    """Process a deposit payment for a sale.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == 'POST':
        imei_number = request.POST.get('device_imei', None)
        if imei_number:
            main_storage = MainStorage.objects.get(device_imei=imei_number)
            data = AccountManager.objects.get(device_imei=imei_number)
            if main_storage:
                main_storage.deposit_paid = True
                data.paid = True
                data.date_updated = timezone.now()
                data.save()
                if main_storage.contract_no != '##':
                    main_storage.pending = False
                message.success(request, 'Deposit payment processed successfully.')
                payload = {
                    'head': 'Deposit Payment',
                    'body': 'Hello {}, Deposit payment for device {} of contract {} has been processed.'.format(
                        main_storage.agent.username, main_storage.device_imei, data.contract),
                    'icon': 'https://raw.githubusercontent.com/Mcnores-Samuel/Hafeez_management_system/main/system_core_1/static/images/logo.png',
                    } 
                user = main_storage.agent
                send_user_notification(user=user, payload=payload, ttl=1000)
                admin = UserProfile.objects.filter(is_superuser=True, is_staff=True)
                staff_members = UserProfile.objects.filter(groups__name='staff_members')
                payload['head'] = 'Deposit Payment'
                payload['body'] = 'Hello Team!, Deposit payment for device {} of contract {} has been processed.'.format(
                        main_storage.device_imei, data.contract)
                for staff in admin:
                    send_user_notification(user=staff, payload=payload, ttl=1000)
                for staff in staff_members:
                    send_user_notification(user=staff, payload=payload, ttl=1000)
                main_storage.save()
            return redirect('pending_deposit_payments')
    return redirect('dashboard')
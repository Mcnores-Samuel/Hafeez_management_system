"""This module contains a view function for the staff operations page, which displays
the operations for the staff members in the system.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from webpush import send_user_notification
from os import environ
from ..models.user_profile import UserProfile
from ..models.account_manager import AccountManager
from ..models.main_storage import MainStorage
from django.urls import reverse


@login_required
def contract_payment(request):
  """This view is used to process the payment for a contract."""
  if request.method == 'POST' and request.user.is_authenticated:
    contract = request.POST.get('contract')
    contract_id = request.POST.get('contract_id')
    mbo = request.POST.get('mbo')
    contract_data = AccountManager.objects.get(contract=contract, id=contract_id)
    contract_data.paid = True
    contract_data.date_updated = timezone.now()
    contract_data.save()
    messages.success(request, 'Payment for contract {} processed successfully.'.format(contract))
    payload = {'head': 'Contract Payment', 'body': 'Hello Team!, Payment for contract {} has been processed'.format(
      contract),
               'icon': '/static/images/logo.png', 'url': 'www.hafeezmw.com'}
    staff_members = UserProfile.objects.filter(groups__name='staff_members')
    for staff in staff_members:
      send_user_notification(user=staff, payload=payload, ttl=1000)
      url = reverse('mbo_data', args=[mbo])
  return redirect(url)


@login_required
def device_locking(request):
  """This view is used to lock a device."""
  if request.method == 'POST' and request.user.is_authenticated:
    contract = request.POST.get('contract')
    contract_id = request.POST.get('contract_id')
    mbo = request.POST.get('mbo')
    contract_data = AccountManager.objects.get(contract=contract, id=contract_id)
    contract_data.locked = True
    device = MainStorage.objects.get(device_imei=contract_data.device_imei)
    device.is_locked = True
    device.save()
    contract_data.save()
    messages.success(request, 'Device {} locked successfully.'.format(contract_data.device_imei))
    admin = UserProfile.objects.filter(is_superuser=True, is_staff=True)
    payload = {'head': 'Device Locked', 'body': 'Hello Team!, Device {} has been locked by MBO {}. Contract: {}, please pay the deposit.'.format(
      contract_data.device_imei, mbo, contract),
               'icon': 'https://raw.githubusercontent.com/Mcnores-Samuel/Hafeez_management_system/main/system_core_1/static/images/logo.png'}
    for staff in admin:
      send_user_notification(user=staff, payload=payload, ttl=1000)
    url = reverse('mbo_data', args=[mbo])
  return redirect(url)
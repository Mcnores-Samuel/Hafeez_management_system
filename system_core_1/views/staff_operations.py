"""This module contains a view function for the staff operations page, which displays
the operations for the staff members in the system.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from webpush import send_user_notification
from os import environ
from ..models.user_profile import UserProfile
from ..models.account_manager import AccountManager
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
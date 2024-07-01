"""This module contains the views for the MBO operations."""
from ..models.account_manager import AccountManager
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from webpush import send_user_notification
from os import environ
from ..models.user_profile import UserProfile
from ..models.main_storage import MainStorage
from django.conf import settings


@login_required
def approve_contract(request):
  """This view is used to approve a contract."""
  if (request.method == 'POST' and request.user.is_authenticated and
      request.user.groups.filter(name='MBOs').exists()):
    contract = request.POST.get('contract')
    contract_id = request.POST.get('contract_id')
    contract_data = AccountManager.objects.get(
      mbo=request.user, contract=contract, id=contract_id)
    contract_data.approved = True
    contract_data.pending = False
    contract_data.date_updated = timezone.now()
    contract_data.date_approved = timezone.now()
    data = MainStorage.objects.get(device_imei=contract_data.device_imei)
    data.mbo_approved = True
    data.save()
    contract_data.save()
    messages.success(request, 'Contract {} approved successfully.'.format(contract))
    payload = {'head': 'Contract Approval', 'body': 'Hello Team!, Contract {}, IMEI: {} has been approved'.format(
      contract, contract_data.device_imei),
               'icon': settings.STATIC_URL + 'images/logo.png', 'url': 'www.hafeezmw.com'}
    staff_members = UserProfile.objects.filter(groups__name='staff_members')
    for staff in staff_members:
      send_user_notification(user=staff, payload=payload, ttl=1000)
  return redirect('pending_contracts')


@login_required
def reject_contract(request):
  """This view is used to reject a contract."""
  if (request.method == 'POST' and request.user.is_authenticated and
      request.user.groups.filter(name='MBOs').exists()):
    contract = request.POST.get('contract')
    contract_id = request.POST.get('contract_id')
    rejected_reason = request.POST.get('rejection_reason')
    issue_description = request.POST.get('issue_description')
    rejection_image = request.FILES.get('rejection_image')
    contract_data = AccountManager.objects.get(
      mbo=request.user, contract=contract, id=contract_id)
    contract_data.rejected = True
    contract_data.pending = False
    if rejected_reason:
      contract_data.rejected_reason = rejected_reason
    if issue_description:
      contract_data.issue_description = issue_description
      contract_data.issue = True
    if rejection_image:
      contract_data.rejected_proof = rejection_image
    contract_data.date_updated = timezone.now()
    data = MainStorage.objects.get(device_imei=contract_data.device_imei)
    data.mbo_rejected = True
    data.save()
    contract_data.save()
    messages.success(request, 'Contract {} rejected successfully.'.format(contract))
    payload = {'head': 'Contract Rejection', 'body': 'Contract {}, IMEI: {} has been rejected'.format(
      contract, contract_data.device_imei),
               'icon': settings.STATIC_URL + 'images/logo.png', 'url': 'www.hafeezmw.com'}
    staff_members = UserProfile.objects.filter(groups__name='staff_members')
    admin = UserProfile.objects.filter(is_superuser=True)
    for staff in staff_members:
      send_user_notification(user=staff, payload=payload, ttl=1000)
    for admin in admin:
      send_user_notification(user=admin, payload=payload, ttl=1000)
  return redirect('pending_contracts')


@login_required
def revert_contract(request):
  """This view is used to revert a contract."""
  if (request.method == 'POST' and request.user.is_authenticated and
      request.user.groups.filter(name='MBOs').exists()):
    contract = request.POST.get('contract')
    contract_id = request.POST.get('contract_id')
    contract_data = AccountManager.objects.get(
      mbo=request.user, contract=contract, id=contract_id)
    contract_data.rejected = False
    contract_data.approved = False
    contract_data.pending = True
    contract_data.date_updated = timezone.now()
    contract_data.save()
    messages.success(request, 'Contract {} reverted successfully.'.format(contract))
    payload = {'head': 'Contract Reversion', 'body': 'Hello Team!, Contract {}, IMEI: {} has been reverted'.format(
      contract, contract_data.device_imei),
               'icon': settings.STATIC_URL + 'images/logo.png', 'url': 'www.hafeezmw.com'}
    staff_members = UserProfile.objects.filter(groups__name='staff_members')
    for staff in staff_members:
      send_user_notification(user=staff, payload=payload, ttl=1000)
  return redirect('pending_contracts')


@login_required
def add_note_to_contract(request):
  """This view is used to add a note to a contract."""
  if (request.method == 'POST' and request.user.is_authenticated and
      request.user.groups.filter(name='MBOs').exists()):
    contract_id = request.POST.get('contract_id')
    note = request.POST.get('important_note')
    contract_data = AccountManager.objects.get(
      mbo=request.user, id=contract_id)
    contract_data.important_note = note
    contract_data.date_updated = timezone.now()
    contract_data.save()
    messages.success(request, 'Note added to contract {} successfully.'.format(contract_data.contract))
    payload = {'head': 'Contract Note', 'body': 'Hello Team!, Note added to contract {}, IMEI: {}.\n{}'.format(
      contract_data.contract, contract_data.device_imei, note), 'icon': settings.STATIC_URL + 'images/logo.png',
      'url': 'www.hafeezmw.com'}
    staff_members = UserProfile.objects.filter(groups__name='staff_members')
    admin = UserProfile.objects.filter(groups__name='admin')
    for staff in staff_members:
      send_user_notification(user=staff, payload=payload, ttl=1000)
    for admin in admin:
      send_user_notification(user=admin, payload=payload, ttl=1000)
  return redirect('pending_contracts')


@login_required
def get_total_pending_contracts(request):
  """This view is used to get the total number of pending contracts."""
  if (request.method == 'GET' and request.user.is_authenticated and
      request.user.groups.filter(name='MBOs').exists()):
    total_pending_contracts = AccountManager.objects.filter(
      mbo=request.user, pending=True, approved=False, rejected=False,
      issue=False).count()
    payload = {'head': 'Pending Contracts', 'body': 'Hello {}!, You have {} pending contracts'.format(
      request.user.username, total_pending_contracts
    ), 'icon': settings.STATIC_URL + 'images/logo.png', 'url': 'www.hafeezmw.com'}
    if total_pending_contracts > 0:
      send_user_notification(user=request.user, payload=payload, ttl=1000)
    return JsonResponse({'total_pending_contracts': total_pending_contracts}, safe=False)
  return JsonResponse({'total_pending_contracts': 0})


@login_required
def get_total_approved_contracts(request):
  """This view is used to get the total number of approved contracts."""
  if (request.method == 'GET' and request.user.is_authenticated and
      request.user.groups.filter(name='MBOs').exists()):
    current_month = timezone.now().date().month
    current_year = timezone.now().date().year
    total_approved_contracts = AccountManager.objects.filter(
      mbo=request.user, pending=False, approved=True, rejected=False,
      issue=False, date_approved__month=current_month,
      date_approved__year=current_year).count()
    return JsonResponse({'total_approved_contracts': total_approved_contracts}, safe=False)
  return JsonResponse({'total_approved_contracts': 0}, safe=False)


@login_required
def get_total_rejected_contracts(request):
  """This view is used to get the total number of rejected contracts."""
  if (request.method == 'GET' and request.user.is_authenticated and
      request.user.groups.filter(name='MBOs').exists()):
    current_month = timezone.now().date().month
    current_year = timezone.now().date().year
    total_rejected_contracts = AccountManager.objects.filter(
      mbo=request.user, pending=False, approved=False, rejected=True,
      issue=False, date_approved__month=current_month,
      date_approved__year=current_year).count()
    return JsonResponse({'total_rejected_contracts': total_rejected_contracts}, safe=False)
  return JsonResponse({'total_rejected_contracts': 0}, safe=False)
"""This module contains the views for the MBO operations."""
from ..models.account_manager import AccountManager
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages



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
    contract_data.save()
    messages.success(request, 'Contract {} approved successfully.'.format(contract))
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
    contract_data.save()
    messages.success(request, 'Contract {} rejected successfully.'.format(contract))
  return redirect('pending_contracts')

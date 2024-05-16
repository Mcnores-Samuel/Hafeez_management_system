from ...models.account_manager import AccountManager
from ...models.user_profile import UserProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q


class AccountManagerDataQuery:
    """This class contains methods for querying the database
    for data to be used by the account manager app.
    """
    def __init__(self, *args, **kwargs):
        pass

    def pending_contracts(self, user, request):
        """Returns a list of pending contracts."""
        if user.groups.filter(name='MBOs').exists():
            account_manager = UserProfile.objects.get(user=user)
            if account_manager:
                pending_contracts = AccountManager.objects.filter(
                    mbo=user, pending=True, active=True,
                    approved=False, rejected=False,
                    issue=False).all().order_by('-date_created')
                paginator = Paginator(pending_contracts, 12)
                page_number = request.GET.get('page')

                try:
                    pending_contracts = paginator.page(page_number)
                except PageNotAnInteger:
                    pending_contracts = paginator.page(1)
                except EmptyPage:
                    pending_contracts = paginator.page(paginator.num_pages)
                return pending_contracts
        return None
    
    def approved_contracts(self, user, request):
        """Returns a list of approved contracts."""
        if user.groups.filter(name='MBOs').exists():
            account_manager = UserProfile.objects.get(user=user)
            if account_manager:
                approved_contracts = AccountManager.objects.filter(
                    mbo=user, pending=False, active=True,
                    approved=True, rejected=False,
                    issue=False).all().order_by('-date_created')
                paginator = Paginator(approved_contracts, 12)
                page_number = request.GET.get('page')

                try:
                    approved_contracts = paginator.page(page_number)
                except PageNotAnInteger:
                    approved_contracts = paginator.page(1)
                except EmptyPage:
                    approved_contracts = paginator.page(paginator.num_pages)
                return approved_contracts
        return None
    
    def rejected_contracts(self, user, request):
        """Returns a list of rejected contracts."""
        if user.groups.filter(name='MBOs').exists():
            account_manager = UserProfile.objects.get(user=user)
            if account_manager:
                rejected_contracts = AccountManager.objects.filter(
                    mbo=user, pending=False, active=True,
                    approved=False, rejected=True,
                    issue=False).all().order_by('-date_created')
                paginator = Paginator(rejected_contracts, 12)
                page_number = request.GET.get('page')

                try:
                    rejected_contracts = paginator.page(page_number)
                except PageNotAnInteger:
                    rejected_contracts = paginator.page(1)
                except EmptyPage:
                    rejected_contracts = paginator.page(paginator.num_pages)
                return rejected_contracts
        return None
    
    def active_issues(self, user, request):
        """Returns a list of active issues."""
        if user.groups.filter(name='MBOs').exists():
            account_manager = UserProfile.objects.get(user=user)
            if account_manager:
                active_issues = AccountManager.objects.filter(
                    mbo=user, pending=False, active=True,
                    approved=False, rejected=False,
                    issue=True).all().order_by('-date_created')
                paginator = Paginator(active_issues, 12)
                page_number = request.GET.get('page')

                try:
                    active_issues = paginator.page(page_number)
                except PageNotAnInteger:
                    active_issues = paginator.page(1)
                except EmptyPage:
                    active_issues = paginator.page(paginator.num_pages)
                return active_issues
        return None
    
    def resolved_issues(self, user, request):
        """Returns a list of resolved issues."""
        if user.groups.filter(name='MBOs').exists():
            account_manager = UserProfile.objects.get(user=user)
            if account_manager:
                resolved_issues = AccountManager.objects.filter(
                    mbo=user, pending=False, active=True,
                    approved=False, rejected=False,
                    issue=True, resolved=True).all().order_by('-date_created')
                paginator = Paginator(resolved_issues, 12)
                page_number = request.GET.get('page')

                try:
                    resolved_issues = paginator.page(page_number)
                except PageNotAnInteger:
                    resolved_issues = paginator.page(1)
                except EmptyPage:
                    resolved_issues = paginator.page(paginator.num_pages)
                return resolved_issues
        return None
    
    def search_contracts(self, user, request):
        """Returns a list of contracts based on a search query."""
        if user.groups.filter(name='MBOs').exists():
            account_manager = UserProfile.objects.get(user=user)
            if account_manager:
                search_query = request.GET.get('search')
                if search_query:
                    contracts = AccountManager.objects.filter(
                        Q(contract__icontains=search_query) |
                        Q(device_imei__icontains=search_query) |
                        Q(device_name__icontains=search_query)).all().order_by('-date_created')
                    paginator = Paginator(contracts, 12)
                    page_number = request.GET.get('page')

                    try:
                        contracts = paginator.page(page_number)
                    except PageNotAnInteger:
                        contracts = paginator.page(1)
                    except EmptyPage:
                        contracts = paginator.page(paginator.num_pages)
                    return contracts
        return None
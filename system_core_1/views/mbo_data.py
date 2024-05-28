"""This module contains a view function for the MBO data page, which displays the
data for the MBOs in the system.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models.account_manager import AccountManager
from ..models.user_profile import UserProfile
from ..data_query_engine.mbos_queries.mbos_data_queries import AccountManagerDataQuery



@login_required
def mbo_data(request, username):
    """
    The `mbo_data` view function displays the data for the MBOs in the system.

    Functionality:
    - Checks if the user is authenticated and has the appropriate permissions.
    - Retrieves the data for the MBOs in the system.
    - Renders the MBO data page, displaying the data for the MBOs.

    Parameters:
    - request: The HTTP request object containing user information.
    - mbo_id: The ID of the MBO for which to display data.

    Returns:
    - Renders the MBO data page, displaying the data for the MBOs.
    - Redirects unauthenticated users to the sign-in page.

    Usage:
    - Authenticated users access this view to view the data for the MBOs in the system.
    - Displays the data for the MBOs, including contract details, device information, etc.

    Note:
    - User authentication and authorization should be managed by the authentication
      and authorization systems.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='staff_members').exists():
        mbo = UserProfile.objects.get(username=username)
        mbos = UserProfile.objects.filter(groups__name='MBOs').all()
        pending_contracts = AccountManager.objects.filter(
            mbo=mbo, approved=False, rejected=False, issue=False
        )
        approved_contracts = AccountManager.objects.filter(
            mbo=mbo, approved=True, rejected=False, issue=False
        )
        issues = AccountManager.objects.filter(
            mbo=mbo, issue=True, resolved=False
        )
        context = {
            'mbo': mbo,
            'pending_contracts': pending_contracts,
            'approved_contracts': approved_contracts,
            'issues': issues,
            'mbos': mbos
        }
    return render(request, 'users/staff_sites/mbo_data.html', context)


@login_required
def pending_contracts(request):
    """
    The `pending_contracts` view function displays the pending contracts for the MBOs.

    Functionality:
    - Checks if the user is authenticated and has the appropriate permissions.
    - Retrieves the pending contracts for the MBOs in the system.
    - Renders the pending contracts page, displaying the pending contracts.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - Renders the pending contracts page, displaying the pending contracts.
    - Redirects unauthenticated users to the sign-in page.

    Usage:
    - Authenticated users access this view to view the pending contracts for the MBOs.
    - Displays the pending contracts for the MBOs, including contract details, etc.

    Note:
    - User authentication and authorization should be managed by the authentication
      and authorization systems.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='MBOs').exists():
        pending_contracts = AccountManagerDataQuery().pending_contracts(request.user, request)
        context = {
            'pending_contracts': pending_contracts
        }
    return render(request, 'users/mbos/pending_contracts.html', context)


@login_required
def approved_contracts(request):
    """
    The `approved_contracts` view function displays the approved contracts for the MBOs.

    Functionality:
    - Checks if the user is authenticated and has the appropriate permissions.
    - Retrieves the approved contracts for the MBOs in the system.
    - Renders the approved contracts page, displaying the approved contracts.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - Renders the approved contracts page, displaying the approved contracts.
    - Redirects unauthenticated users to the sign-in page.

    Usage:
    - Authenticated users access this view to view the approved contracts for the MBOs.
    - Displays the approved contracts for the MBOs, including contract details, etc.

    Note:
    - User authentication and authorization should be managed by the authentication
      and authorization systems.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='MBOs').exists():
        approved_contracts = AccountManagerDataQuery().approved_contracts(request.user, request)
        context = {
            'approved_contracts': approved_contracts
        }
    return render(request, 'users/mbos/approved_contracts.html', context)


@login_required
def search_contracts(request):
    """
    The `search_contracts` view function displays the search results for the MBOs.

    Functionality:
    - Checks if the user is authenticated and has the appropriate permissions.
    - Retrieves the search results for the MBOs in the system.
    - Renders the search results page, displaying the search results.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - Renders the search results page, displaying the search results.
    - Redirects unauthenticated users to the sign-in page.

    Usage:
    - Authenticated users access this view to view the search results for the MBOs.
    - Displays the search results for the MBOs, including contract details, etc.

    Note:
    - User authentication and authorization should be managed by the authentication
      and authorization systems.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='MBOs').exists():
        search_results = AccountManagerDataQuery().search_contracts(request.user, request)
        context = {
            'search_results': search_results
        }
    return render(request, 'users/mbos/search_contracts.html', context)



@login_required
def rejected_contracts(request):
    """
    The `rejected_contracts` view function displays the rejected contracts for the MBOs.

    Functionality:
    - Checks if the user is authenticated and has the appropriate permissions.
    - Retrieves the rejected contracts for the MBOs in the system.
    - Renders the rejected contracts page, displaying the rejected contracts.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - Renders the rejected contracts page, displaying the rejected contracts.
    - Redirects unauthenticated users to the sign-in page.

    Usage:
    - Authenticated users access this view to view the rejected contracts for the MBOs.
    - Displays the rejected contracts for the MBOs, including contract details, etc.

    Note:
    - User authentication and authorization should be managed by the authentication
      and authorization systems.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='MBOs').exists():
        rejected_contracts = AccountManagerDataQuery().rejected_contracts(request.user, request)
        context = {
            'rejected_contracts': rejected_contracts
        }
    return render(request, 'users/mbos/rejected_contracts.html', context)


@login_required
def active_issues(request):
    """
    The `active_issues` view function displays the active issues for the MBOs.

    Functionality:
    - Checks if the user is authenticated and has the appropriate permissions.
    - Retrieves the active issues for the MBOs in the system.
    - Renders the active issues page, displaying the active issues.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - Renders the active issues page, displaying the active issues.
    - Redirects unauthenticated users to the sign-in page.

    Usage:
    - Authenticated users access this view to view the active issues for the MBOs.
    - Displays the active issues for the MBOs, including issue details, etc.

    Note:
    - User authentication and authorization should be managed by the authentication
      and authorization systems.
    """
    if request.user.is_authenticated and request.user.groups.filter(name='MBOs').exists():
        active_issues = AccountManagerDataQuery().active_issues(request.user, request)
        context = {
            'active_issues': active_issues
        }
    return render(request, 'users/mbos/active_issues.html', context)
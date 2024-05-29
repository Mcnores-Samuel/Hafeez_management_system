"""This module contains a view function for the MBO data analysis page, which displays
the data analysis for the MBOs in the system.
"""
from django.contrib.auth.decorators import login_required
from ..models.account_manager import AccountManager
from ..models.user_profile import UserProfile
from django.http import JsonResponse
from django.utils import timezone



@login_required
def daily_approved_contracts(request):
    """
    The `daily_approved_contracts` view function displays the daily approved contracts
    for the MBOs in the system.

    Functionality:
    - Checks if the user is authenticated and has the appropriate permissions.
    - Retrieves the daily approved contracts for the MBOs in the system.
    - Renders the daily approved contracts page, displaying the data analysis.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - Renders the daily approved contracts page, displaying the data analysis.
    - Redirects unauthenticated users to the sign-in page.

    Usage:
    - Authenticated users access this view to view the daily approved contracts data analysis.
    - Displays the daily approved contracts data analysis for the MBOs in the system.
    """
    if request.method == 'GET':
        today = timezone.now().date()
        mbo = UserProfile.objects.get(id=request.user.id)
        approved_contracts = AccountManager.objects.filter(
            mbo=mbo, approved=True, date_updated__date=today, active=True,
            rejected=False, issue=False
        )
        sales = {}
        for contract in approved_contracts:
            sales[contract.device_name] = sales.get(contract.device_name, 0) + 1
        return JsonResponse(sales, safe=False)
    


@login_required
def weekly_approved_contracts(request):
    """
    The `weekly_approved_contracts` view function displays the weekly approved contracts
    for the MBOs in the system.

    Functionality:
    - Checks if the user is authenticated and has the appropriate permissions.
    - Retrieves the weekly approved contracts for the MBOs in the system.
    - Renders the weekly approved contracts page, displaying the data analysis.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - Renders the weekly approved contracts page, displaying the data analysis.
    - Redirects unauthenticated users to the sign-in page.

    Usage:
    - Authenticated users access this view to view the weekly approved contracts data analysis.
    - Displays the weekly approved contracts data analysis for the MBOs in the system.
    """
    if request.method == 'GET':
        current_week = timezone.now().date()
        week_days = ['Monday', 'Tuesday', 'Wednesday',
                     'Thursday', 'Friday', 'Saturday',
                     'Sunday']
        days = {day: [] for day in week_days}
        monday = current_week - timezone.timedelta(
            days=current_week.weekday())
        sunday = monday + timezone.timedelta(days=6)
        mbo = UserProfile.objects.get(id=request.user.id)
        approved_contracts = AccountManager.objects.filter(
            mbo=mbo, approved=True, date_updated__range=[monday, sunday],
            active=True, rejected=False, issue=False
        )
        for contract in approved_contracts:
            item = {'device_name': contract.device_name}
            days[week_days[contract.date_updated.weekday()]].append(item)
            item = {}
        return JsonResponse(days, safe=False)
    


@login_required
def yearly_approved_contracts(request):
    """
    The `yearly_approved_contracts` view function displays the yearly approved contracts
    for the MBOs in the system.

    Functionality:
    - Checks if the user is authenticated and has the appropriate permissions.
    - Retrieves the yearly approved contracts for the MBOs in the system.
    - Renders the yearly approved contracts page, displaying the data analysis.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - Renders the yearly approved contracts page, displaying the data analysis.
    - Redirects unauthenticated users to the sign-in page.

    Usage:
    - Authenticated users access this view to view the yearly approved contracts data analysis.
    - Displays the yearly approved contracts data analysis for the MBOs in the system.
    """
    if request.method == 'GET':
        months = ['January', 'February', 'March', 'April', 'May',
            'June', 'July', 'August', 'September', 'October',
            'November', 'December']
        sales_by_month = {}
        mbo = UserProfile.objects.get(id=request.user.id)
        current_year = timezone.now().date().year
        for month in months:
            sales_by_month[month] = AccountManager.objects.filter(
                mbo=mbo, approved=True, date_updated__month=months.index(month) + 1,
                date_updated__year=current_year, active=True, rejected=False,
                issue=False
            ).count()
    return JsonResponse(sales_by_month, safe=False)
    
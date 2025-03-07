from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from system_core_1.models.main_storage import MainStorage
from system_core_1.models.user_profile import UserProfile
from system_core_1.models.cost_per_invoice import CostPerInvoice
from django.http import JsonResponse
import json


@login_required
@csrf_exempt
def dispatch_stock(request):
    """This view function is responsible for dispatching stock to agents.

    Functionality:
    - Checks if the user is authenticated.
    - Renders the dispatch stock page.
    - Allows dispatching multiple stock items to agents.
    - Provides options to filter agents and stock items.
    - Allows the user to select agents and stock items for dispatch.
    - Validates the dispatch request and updates the stock and agent records.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - Renders the dispatch stock page.
    - Redirects unauthenticated users to the login page.

    Usage:
    - Authenticated users access this view to dispatch stock to agents.
    - The view provides options to filter agents and stock items for dispatch.
    - The user can select agents and stock items for dispatch.
    - The view validates the dispatch request and updates the stock and agent records.

    Note:
    - User authentication and authorization should be managed by the authentication
      and authorization systems.
    """
    if request.method == 'POST' and request.user.is_staff and request.user.is_superuser\
        or request.user.groups.filter(name='branches').exists() and request.method == 'POST':
        data = request.POST.get('data', None)
        date = request.POST.get('date', None)
        agent = request.POST.get('agent', None)
        if data:
            scanned_items = json.loads(data)
            date = json.loads(date)
            agent = json.loads(agent)
            not_in_stock = []
            invoice_items = []
            user = UserProfile.objects.get(username=agent)
            for item in scanned_items:
                try:
                    stock_item = MainStorage.objects.get(device_imei=item)
                    stock_item.collected_on = date
                    stock_item.recieved = True
                    stock_item.agent = user
                    if user.groups.filter(name='partners').exists():
                        invoice_items.append(stock_item)
                    stock_item.save()
                except MainStorage.DoesNotExist:
                    not_in_stock.append(item)
            if invoice_items:
                cost_per_invoice = CostPerInvoice.objects.create(
                    partner=user, invoice_date=date, created_at=date, updated_at=date,
                    original_cost=0.0, cost_per_ex_rate=0.0, total_items_sold=0,
                    last_payment_amount=0.0, last_payment_date=date, current_balance=0.0,
                    total_amount_paid=0.0, is_paid=False)
                cost_per_invoice.attach_items(invoice_items)
                cost_per_invoice.save()
            return JsonResponse({'status': 200, 'not_in_stock': not_in_stock})
        else:
            return JsonResponse({'status': 400, 'error': 'No data received'})
    agents = UserProfile.objects.filter(groups__name='agents')
    agents = sorted(agents, key=lambda x: x.username)
    special_outlets = UserProfile.objects.filter(groups__name='partners')
    branches = UserProfile.objects.filter(groups__name='branches')
    agents = list(set(agents + sorted(special_outlets, key=lambda x: x.username)\
                      + sorted(branches, key=lambda x: x.username)))
    if request.user.groups.filter(name='branches').exists():
        return render(request, 'users/branches/dispatch.html', {'agents': agents})
    return render(request, 'users/admin_sites/dispatch.html', {'agents': sorted(agents, key=lambda x: x.username)})

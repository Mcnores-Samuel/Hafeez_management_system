"""This module contains the views related to the pending sales."""
from ..data_analysis_engine.admin_panel.mainstorage_analysis import MainStorageAnalysis
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models.main_storage import MainStorage
from django.contrib import messages as message
from django.http import JsonResponse


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
            if approved:
                if (approved[0].sales_type == 'Loan'
                    and approved[0].contract_no != '##'):
                    name = approved[0].name
                    approved.update(pending=False)
                    message.success(request, '{} of {} The sale has been approved.'.format(
                        name, device))
                    return redirect('pending_sales')
                elif (approved[0].sales_type == 'Cash'):
                    name = approved[0].name
                    approved.update(pending=False)
                    message.success(request, '{} of {} The sale has been approved.'.format(
                        name, device))
                    return redirect('pending_sales')
                else:
                    message.warning(request, 'Please update the Contract Number to approve the sale.')
                return redirect('pending_sales')
    if request.user.is_staff and  request.user.is_superuser:
        analysis = MainStorageAnalysis()
        pending_sales, total = analysis.pending_sales()
        return render(request, 'users/admin_sites/pending_sales.html',
                      {'pending_sales': pending_sales, 'total': total})
    

def total_pending_sales(request):
    """Returns the total pending sales.

    Returns:
        int: The total pending sales.
    """
    if request.method == 'GET':
        total = MainStorage.objects.filter(
            pending=True, sold=True, in_stock=False).count()
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
                    main_storage.save()
                    message.success(request, 'device reverted to stock successfully')
                return redirect('pending_sales')
    return redirect('dashboard')

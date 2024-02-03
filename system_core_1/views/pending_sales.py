"""This module contains the views related to the pending sales."""
from ..data_analysis_engine.admin_panel.mainstorage_analysis import MainStorageAnalysis
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models.main_storage import MainStorage


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
                approved.update(pending=False)
                return redirect('pending_sales')
    if request.user.is_staff and  request.user.is_superuser:
        analysis = MainStorageAnalysis()
        pending_sales, total = analysis.pending_sales()
        return render(request, 'users/admin_sites/pending_sales.html',
                      {'pending_sales': pending_sales, 'total': total})
"""This module contains a view for the liabilities json response."""
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from system_core_1.models.expenses import Liability


@login_required
def total_liabilities(request):
    """This function returns the total liabilities."""
    if request.method == 'GET' and request.user.is_superuser:
        total = Liability.total_current_liabilities() + Liability.total_non_current_liabilities()
        return JsonResponse({'total_liabilities': total})
    return JsonResponse({'error': 'Invalid request.'})
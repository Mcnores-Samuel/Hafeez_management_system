"""This module contains the views for revenue data."""
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from system_core_1.models.main_storage import MainStorage
from django.utils import timezone
from django.db.models import Sum


@login_required
def current_year_revenue(request):
    """Retruns the total revenue for the current year including other data calculations."""
    if request.method == 'GET' and request.user.is_superuser:
        current_year = timezone.now().year
        data = MainStorage.objects.filter(stock_out_date__year=current_year, agent__groups__name='agents',
            in_stock=False, sold=True, missing=False, pending=False, assigned=True
        )
        total = data.count()
        items_with_both_ps = data.filter(price__isnull=False, cost__isnull=False)
        t_items_wbps = items_with_both_ps.count()
        revenue_for_itwbps = items_with_both_ps.aggregate(
            total_revenue=Sum('price'),
            total_cost=Sum('cost')
        )

        return JsonResponse({'year': current_year, 'total_calculated': total, 'total_items_with_both_ps': t_items_wbps,
                             'revenue': revenue_for_itwbps['total_revenue'], 'cost': revenue_for_itwbps['total_cost']})
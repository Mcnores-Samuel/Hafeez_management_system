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
        items_with_both_ps = data.filter(price__gt=0, cost__gt=0)
        t_items_wbps = items_with_both_ps.count()
        revenue_for_itwbps = items_with_both_ps.aggregate(
            total_revenue=Sum('price'),
            total_cost=Sum('cost')
        )

        items_with_cost_only = data.filter(price=0, cost__gt=0)
        total_items_with_cost_only = items_with_cost_only.count()
        revenue_for_itwco = items_with_cost_only.aggregate(
            total_revenue=Sum('price'),
            total_cost=Sum('cost')
        )

        items_with_price_only = data.filter(price__gt=0, cost=0)
        total_items_with_price_only = items_with_price_only.count()
        revenue_for_itwpo = items_with_price_only.aggregate(
            total_revenue=Sum('price'),
            total_cost=Sum('cost')
        )

        items_with_no_ps = data.filter(price=0, cost=0)
        total_items_with_no_ps = items_with_no_ps.count()
        revenue_for_itwnps = items_with_no_ps.aggregate(
            total_revenue=Sum('price'),
            total_cost=Sum('cost')
        )

        context = {
            'year': current_year,
            'total_calculated': total,
            'both_price_and_cost': t_items_wbps,
            'revenue': revenue_for_itwbps['total_revenue'],
            'cost': revenue_for_itwbps['total_cost'],
            'cost_only': total_items_with_cost_only,
            'revenue_for_itwco': revenue_for_itwco['total_revenue'],
            'cost_for_itwco': revenue_for_itwco['total_cost'],
            'price_only': total_items_with_price_only,
            'revenue_for_itwpo': revenue_for_itwpo['total_revenue'],
            'cost_for_itwpo': revenue_for_itwpo['total_cost'],
            'no_price_or_cost': total_items_with_no_ps,
            'revenue_for_itwnps': revenue_for_itwnps['total_revenue'],
            'cost_for_itwnps': revenue_for_itwnps['total_cost']
        }

        return JsonResponse(context)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def revenue_by_category(request):
    """Returns the total revenue for the current year by category."""
    if request.method == 'GET' and request.user.is_superuser:
        current_year = timezone.now().year
        categories = set()
        data = MainStorage.objects.filter(stock_out_date__year=current_year, agent__groups__name='agents',
            in_stock=False, sold=True, missing=False, pending=False, assigned=True, cost__gt=0, price__gt=0,
        )
        for item in data:
            categories.add(item.category)
        categories = list(categories)
        revenueByCategory = []
        for category in categories:
            items = data.filter(category=category)
            total = sum([item.price for item in items])
            revenueByCategory.append(
                {
                    'category': category,
                    'total_revenue': total,
                    'total_items': items.count()
                }
            )
        return JsonResponse(revenueByCategory, safe=False)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def calculateCreditRevenue(request):
    """Calculate the credit revenue Sort by Month"""
    if request.method == 'GET':
        months = ['January', 'February', 'March', 'April', 'May',
            'June', 'July', 'August', 'September', 'October',
            'November', 'December']
        revenue = {}
        for month in months:
            items = MainStorage.objects.filter(
                in_stock=False, sold=True, pending=False, missing=False, cost__gt=0, price__gt=0,
                assigned=True, sales_type='Loan', stock_out_date__month=months.index(month)+1,
                stock_out_date__year=timezone.now().year)
            total = sum([item.price for item in items])
            revenue[month] = total
        return JsonResponse(revenue, safe=False)
    return JsonResponse({'error': 'Invalid request.'})
"""This module contains the views for revenue data."""
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from system_core_1.models.main_storage import MainStorage
from django.utils import timezone
from django.db.models import Sum


@login_required
def current_year_revenue(request):
    """Retruns the total revenue for the current year including other data calculations."""
    data = None
    current_year = timezone.now().year

    if request.method == 'GET' and request.user.is_superuser:
        data = MainStorage.objects.filter(stock_out_date__year=current_year, agent__groups__name='agents',
            in_stock=False, sold=True, missing=False, pending=False, assigned=True
        )
    elif request.method == 'GET' and request.user.groups.filter(name='branches').exists():
        data = MainStorage.objects.filter(stock_out_date__year=current_year, agent=request.user,
            in_stock=False, sold=True, missing=False, pending=False, assigned=True
        )

    if data is None:
        return JsonResponse({'error': 'Invalid request.'})
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


@login_required
def revenue_by_category(request):
    """Returns the total revenue for the current year by category."""
    current_year = timezone.now().year
    categories = set()
    data = None

    if request.method == 'GET' and request.user.is_superuser:
        data = MainStorage.objects.filter(stock_out_date__year=current_year, agent__groups__name='agents',
            in_stock=False, sold=True, missing=False, pending=False, assigned=True, cost__gt=0, price__gt=0,
        )

    if request.method == 'GET' and request.user.groups.filter(name='branches').exists():
        data = MainStorage.objects.filter(stock_out_date__year=current_year, agent=request.user,
            in_stock=False, sold=True, missing=False, pending=False, assigned=True, cost__gt=0, price__gt=0,
        )
    
    if data is None:
        return JsonResponse({'error': 'Invalid request.'})
    
    for item in data:
        categories.add(item.category)
    categories = list(categories)
    revenueByCategory = []
    for category in categories:
        items = data.filter(category=category)
        cost = items.aggregate(total_cost=Sum('cost'))
        revenue = items.aggregate(total_revenue=Sum('price'))
        revenueByCategory.append(
            {
                'category': category,
                'total_cost': cost['total_cost'],
                'total_revenue': revenue['total_revenue']
            }
        )
    return JsonResponse(revenueByCategory, safe=False)


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


@login_required
def calculateCashRevenue(request):
    """Calculate the cash revenue Sort by Month"""
    if request.method == 'GET':
        months = ['January', 'February', 'March', 'April', 'May',
            'June', 'July', 'August', 'September', 'October',
            'November', 'December']
        revenue = {}
        for month in months:
            items = MainStorage.objects.filter(
                in_stock=False, sold=True, pending=False, missing=False, cost__gt=0, price__gt=0,
                assigned=True, sales_type='Cash', stock_out_date__month=months.index(month)+1,
                stock_out_date__year=timezone.now().year)
            total = sum([item.price for item in items])
            revenue[month] = total
        return JsonResponse(revenue, safe=False)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def lastyearBycurrentMonth(request):
    """Calculate the total revenue for the last year by the current month."""
    if request.method == 'GET':
        current_month = timezone.now().month
        last_year = timezone.now().year - 1
        data = MainStorage.objects.filter(
            in_stock=False, sold=True, missing=False, pending=False, assigned=True,
            stock_out_date__month__lte=current_month,
            stock_out_date__year=last_year, price__gt=0,
            agent__groups__name='agents'
        )
        group_by_month = {}
        for i in range(1, current_month+1):
            items = data.filter(stock_out_date__month=i)
            total = sum([item.price for item in items])
            group_by_month[timezone.datetime(last_year, i, 1).strftime('%B')] = total
        return JsonResponse(group_by_month)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def revenue_growth(request):
    """Calculate the revenue growth."""
    if request.method == 'GET':
        current_year = timezone.now().year
        last_year = current_year - 1
        current_month = timezone.now().month
        current_year_data = MainStorage.objects.filter(
            in_stock=False, sold=True, missing=False, pending=False, assigned=True,
            stock_out_date__year=current_year, price__gt=0, stock_out_date__month__lte=current_month,
            agent__groups__name='agents'
        )
        last_year_data = MainStorage.objects.filter(
            in_stock=False, sold=True, missing=False, pending=False, assigned=True,
            stock_out_date__year=last_year, price__gt=0, stock_out_date__month__lte=current_month,
            agent__groups__name='agents'
        )
        current_year_revenue = sum([item.price for item in current_year_data])
        last_year_revenue = sum([item.price for item in last_year_data])
        if last_year_revenue == 0:
            return JsonResponse({'growth': 100})
        
        if current_year_revenue == 0:
            return JsonResponse({'growth': -100})
        growth = (current_year_revenue - last_year_revenue) / last_year_revenue * 100
        growth = round(growth, 2)
        return JsonResponse({'growth': growth})
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def average_order_value(request):
    """Calculate the average order value."""
    if request.method == 'GET':
        current_year = timezone.now().year
        current_month = timezone.now().month
        data = MainStorage.objects.filter(
            in_stock=False, sold=True, missing=False, pending=False, assigned=True,
            stock_out_date__year=current_year, cost__gt=0, price__gt=0, stock_out_date__month__lte=current_month,
            agent__groups__name='agents'
        )
        total_revenue = sum([item.price for item in data])
        total_orders = data.count()
        if total_orders == 0:
            return JsonResponse({'average_order_value': 0})
        average_order_value = total_revenue / total_orders
        average_order_value = round(average_order_value, 3)
        return JsonResponse({'average_order_value': average_order_value})
    return JsonResponse({'error': 'Invalid request.'})
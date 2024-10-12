from ..models.main_storage import MainStorage
from ..models.user_profile import UserProfile
from django.http import JsonResponse
from django.db.models import Count, Q
from django.shortcuts import render
from ..forms.filters import FilterSalesAndStock
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required
def sales_stock_summry(request):
    """Returns a JSON object containing the daily stock data."""
    if request.method == 'GET':
        agent_id = request.GET.get('agent')
        month = request.GET.get('month')
        year = request.GET.get('year')
        date = request.GET.get('date')
        if agent_id and month and year and date:
            agent = UserProfile.objects.get(id=agent_id)
            actual_date = timezone.datetime.strptime(date, '%Y-%m-%d')

            available_stock = MainStorage.objects.filter(
                agent=agent, in_stock=True, sold=False, assigned=True,
                pending=False, missing=False, recieved=True)
            
            daily_sales_data = MainStorage.objects.filter(
                agent=agent, in_stock=False, sold=True, assigned=True,
                pending=False, missing=False, stock_out_date=actual_date.date())
            
            monthly_sales_data = MainStorage.objects.filter(
                agent=agent, in_stock=False, sold=True, assigned=True,
                pending=False, missing=False, stock_out_date__month=month,
                stock_out_date__year=year)
            
            total_stock = available_stock.count()
            tota_daily_sales = daily_sales_data.count()
            total_monthly_sales = monthly_sales_data.count()
            stock = {}
            daily_sales = {}
            monthly_sales = {}
            monthly_sales_details = []
            stock_details = []

            for data in available_stock:
                stock[data.phone_type] = stock.get(data.phone_type, 0) + 1
                stock_details.append({
                    'category': data.category,
                    'phone_type': data.phone_type,
                    'imei': data.device_imei,
                    'date_collected': data.collected_on,
                    'id': data.id
                })

            for item in daily_sales_data:
                daily_sales[item.phone_type] = daily_sales.get(item.phone_type, 0) + 1

            for sale in monthly_sales_data:
                monthly_sales[sale.phone_type] = monthly_sales.get(sale.phone_type, 0) + 1
                monthly_sales_details.append({
                    'category': sale.category,
                    'phone_type': sale.phone_type,
                    'imei': sale.device_imei,
                    'date_collected': sale.collected_on,
                    'date_sold': sale.stock_out_date,
                    'Sales Type': sale.sales_type
                })

            stock = sorted(stock.items(), key=lambda x: x[1], reverse=True)
            daily_sales = sorted(daily_sales.items(), key=lambda x: x[1], reverse=True)
            monthly_sales = sorted(monthly_sales.items(), key=lambda x: x[1], reverse=True)
            monthly_sales = dict(monthly_sales)
            daily_sales = dict(daily_sales)
            stock = dict(stock)
            content = {
                'data': {
                    'total_stock': total_stock,
                    'total_daily_sales': tota_daily_sales,
                    'total_monthly_sales': total_monthly_sales,
                    'stock': stock,
                    'daily_sales': daily_sales,
                    'monthly_sales': monthly_sales,
                    'monthly_sales_details': monthly_sales_details,
                    'stock_details': stock_details
                }}
            return JsonResponse(content)
        return JsonResponse({'error': 'Invalid request.'})
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def dataAccess(request):
    """Returns a JSON object containing the daily stock data."""
    if request.method == 'GET':
        form = FilterSalesAndStock()
        return render(request, 'users/staff_sites/accounts_and_data.html',
                      {'form': form})
    

@login_required
def dailySalesByShop(request):
    """Returns a JSON object containing the daily stock data."""
    if request.method == 'GET':
        agents = UserProfile.objects.filter(agentprofile__is_agent=True).all().order_by('id')
        daily_sales_pr_shop = agents.annotate(
            total_sales=Count('mainstorage', filter=Q(
                mainstorage__in_stock=False,
                mainstorage__sold=True,
                mainstorage__assigned=True,
                mainstorage__stock_out_date=timezone.now().date()
            ))
        )

        data = []
        for shop in daily_sales_pr_shop:
            if shop.total_sales > 0:
                data.append({
                    'shop': shop.username,
                    'total_sales': shop.total_sales
                })
        return JsonResponse({'data': data})
    return JsonResponse({'error': 'Invalid request.'})


def stock(request, data_id):
    """Returns a JSON object containing the daily stock data."""
    if request.method == 'GET':
        item = MainStorage.objects.get(id=data_id)
        content = {
            'imei': item.device_imei,
            'model': item.phone_type,
            'id': item.id,
        }
    return render(request, 'users/staff_sites/stock.html', content)
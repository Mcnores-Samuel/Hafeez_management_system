from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ...models.user_profile import UserProfile
from ...models.main_storage import MainStorage
from django.contrib.auth.models import Group
from django.utils import timezone
from ...data_analysis_engine.admin_panel.calc_commitions import CalcCommissions
from ...data_analysis_engine.admin_panel.mainstorage_analysis import MainStorageAnalysis


@login_required
def get_source_stock(request):
    """Returns a JSON object containing the daily stock data."""
    if request.method == 'GET':
        main_shop_staff = Group.objects.get(name='main_shop')
        representatives = UserProfile.objects.filter(groups=main_shop_staff)
        data_set = MainStorage.objects.filter(
            agent__in=representatives,
            in_stock=True, sold=False,
            missing=False, assigned=True)
        stock = {}
        for data in data_set:
            stock[data.phone_type] = stock.get(data.phone_type, 0) + 1
        stock = sorted(stock.items(), key=lambda x: x[1], reverse=True)
        return JsonResponse(stock, safe=False)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_yearly_product_sales(request):
    """This function returns a JSON object containing
    the yearly product sales data for overall sales.
    """
    if request.method == 'GET':
        year = timezone.now().date().year
        data_set = MainStorage.objects.filter(
            in_stock=False, assigned=True,
            sold=True, missing=False,
            pending=False, stock_out_date__year=year)
        products = {}
        for product in data_set:
            products[product.phone_type] = products.get(product.phone_type, 0) + 1
        return JsonResponse(products, safe=False)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def admin_stock_analysis(request):
    """This function returns a JSON object containing the daily stock data."""
    if request.method == 'GET':
        progress = 0
        target = 0
        total_sales = 0
        overall_sales = 0
        overall_stock = 0
        main_shop_stock = 0
        if request.user.is_superuser:
            representatives = UserProfile.objects.filter(groups='main_shop').first()
            sales = MainStorageAnalysis().get_agent_stock_out(representatives)
            overall_sales = MainStorageAnalysis().overall_sales(agent=representatives)
            overall_stock = MainStorageAnalysis().overall_stock()
            for value in sales:
                total_sales += value[1]
            CalcCommissions().update_commission(representatives, total_sales)
            progress, target = CalcCommissions().target_progress(representatives)
            main_shop_stock = MainStorage.objects.filter(
                agent=representatives, in_stock=True, sold=False, missing=False,
                assigned=True, available=True).count()
        elif request.user.groups.filter(name='branches').exists():
            representatives = request.user
            sales = MainStorageAnalysis().get_agent_stock_out(representatives)
            overall_sales = MainStorageAnalysis().overall_sales(agent=representatives)
            overall_stock = MainStorageAnalysis().overall_stock(agent=representatives)
            for value in sales:
                total_sales += value[1]
            CalcCommissions().update_commission(representatives, total_sales)
            progress, target = CalcCommissions().target_progress(representatives)
            main_shop_stock = MainStorage.objects.filter(
                agent=representatives, in_stock=True, sold=False, missing=False,
                assigned=True, available=True).count()
        context = {
            'progress': progress,
            'target': target,
            'sales': total_sales,
            'overall_sales': overall_sales,
            'overall_stock': overall_stock,
            'main_shop_stock': main_shop_stock,
        }
        return JsonResponse(context, safe=False)
    return JsonResponse({'error': 'Invalid request.'})

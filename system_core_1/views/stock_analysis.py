from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..models.user_profile import UserProfile
from ..models.main_storage import MainStorage
from django.contrib.auth.models import Group
from django.utils import timezone


@login_required
def get_source_stock(request):
    """Returns a JSON object containing the daily stock data."""
    if request.method == 'GET':
        main_shop_staff = Group.objects.get(name='main_shop')
        representatives = UserProfile.objects.filter(groups=main_shop_staff)
        data_set = MainStorage.objects.filter(agent__in=representatives,
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
        products = sorted(products.items(), key=lambda x: x[1], reverse=True)
        return JsonResponse(products, safe=False)
    return JsonResponse({'error': 'Invalid request.'})
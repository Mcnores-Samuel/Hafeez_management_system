from ..models.main_storage import MainStorage
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..models.agent_profile import AgentProfile
from django.contrib.auth.models import Group
from ..models.user_profile import UserProfile


@login_required
def get_daily_sales_json(request):
    """Returns a JSON object containing the daily sales data."""
    if request.method == 'GET':
        today = timezone.now().date()
        data_set = MainStorage.objects.filter(stock_out_date=today, sold=True, in_stock=False)
        sales = {}
        for data in data_set:
            sales[data.phone_type] = sales.get(data.phone_type, 0) + 1
        return JsonResponse(sales)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_weekly_sales_json(request):
    """Returns a JSON object containing the weekly sales data."""
    if request.method == 'GET':
        current_week = timezone.now().date()
        week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        days = {}
        monday = current_week - timezone.timedelta(days=current_week.weekday())
        sunday = monday + timezone.timedelta(days=6)

        for day in week_days:
            days[day] = []
        
        data_set = MainStorage.objects.filter(stock_out_date__range=[monday, sunday],
                                              sold=True, in_stock=False)
        for data in data_set:
            item = {'type': data.phone_type, 'imei': data.device_imei}
            days[week_days[data.stock_out_date.weekday()]].append(item)
            item = {}
        return JsonResponse(days)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_sale_by_agent_monthy_loan(request):
    """Returns a JSON object containing the monthly sales data by agent."""
    if request.method == 'GET':
        agents = AgentProfile.objects.all().order_by('user__username')
        sales_by_agent = {}
        current_month = timezone.now().date().month
        current_year = timezone.now().date().year
        total_sales = MainStorage.objects.filter(stock_out_date__month=current_month,
                                                 stock_out_date__year=current_year,
                                                 sold=True, in_stock=False, sales_type='Loan',
                                                 missing=False)
        for agent in agents:
            sales_by_agent[str(agent.user.username).lower().capitalize()] = len(MainStorage.objects.filter(agent=agent.user,
                                                                                 stock_out_date__month=current_month,
                                                                                 stock_out_date__year=current_year,
                                                                                 sold=True, in_stock=False, sales_type='Loan',
                                                                                 missing=False))
        sales_by_agent['Total'] = len(total_sales)
        sales_by_agent = sorted(sales_by_agent.items(), key=lambda x: x[1], reverse=True)
        return JsonResponse(sales_by_agent, safe=False)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_sale_by_agent_monthy_cash(request):
    """Returns a JSON object containing the monthly sales data by agent."""
    if request.method == 'GET':
        agents = AgentProfile.objects.all().order_by('user__username')
        sales_by_agent = {}
        current_month = timezone.now().date().month
        current_year = timezone.now().date().year
        total_sales = MainStorage.objects.filter(stock_out_date__month=current_month,
                                                 stock_out_date__year=current_year,
                                                 sold=True, in_stock=False, sales_type='Cash',
                                                 missing=False)
        for agent in agents:
            sales_by_agent[str(agent.user.username).lower().capitalize()] = len(MainStorage.objects.filter(agent=agent.user,
                                                                                 stock_out_date__month=current_month,
                                                                                 stock_out_date__year=current_year,
                                                                                 sold=True, in_stock=False, sales_type='Cash',
                                                                                 missing=False))
        sales_by_agent['Total'] = len(total_sales)
        sales_by_agent = sorted(sales_by_agent.items(), key=lambda x: x[1], reverse=True)
        return JsonResponse(sales_by_agent, safe=False)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_agents_stock_json(request):
    """Returns a JSON object containing the agents and their stocks."""
    if request.method == 'GET':
        agents = AgentProfile.objects.all().order_by('user__username')
        main_shop_staff = Group.objects.get(name='main_shop')
        representatives = UserProfile.objects.filter(groups=main_shop_staff)
        stocks = {}
        total = 0
        for agent in agents:
            if agent.user not in representatives:
                stocks[str(agent.user.username).lower().capitalize()] = len(
                    MainStorage.objects.filter(
                        agent=agent.user, in_stock=True, 
                        sold=False, missing=False, assigned=True))
                total += len(MainStorage.objects.filter(
                    agent=agent.user, in_stock=True, 
                    sold=False, missing=False, assigned=True))
        stocks['Total'] = total
        return JsonResponse(stocks)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_main_stock_analysis(request):
    """Returns a JSON object containing the main stock analysis."""
    if request.method == 'GET':
        main_shop_staff = Group.objects.get(name='main_shop')
        representatives = UserProfile.objects.filter(groups=main_shop_staff)
        data_set = MainStorage.objects.filter(agent__in=representatives,
                                              in_stock=True, sold=False,
                                              missing=False, assigned=True)
        stock = {}
        stock[representatives[0].username] = len(data_set)
        stock['capacity'] = 1000
        stock['Total'] = len(data_set)
        return JsonResponse(stock)
    return JsonResponse({'error': 'Invalid request.'})
from ...models.main_storage import MainStorage
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ...models.agent_profile import AgentProfile
from django.contrib.auth.models import Group
from ...models.user_profile import UserProfile
from ...data_analysis_engine.admin_panel.mainstorage_analysis import MainStorageAnalysis
from ...data_query_engine.agents_queries.agents_data_query import AgentsDataQuery


@login_required
def get_daily_sales(request, sales_type):
    """Returns a JSON object containing the daily sales data."""
    if request.method == 'GET':
        sales = None
        if request.user.groups.filter(name='branches').exists():
            sales = MainStorageAnalysis().get_daily_sales(sales_type=sales_type, agent=request.user)
        else:
            sales = MainStorageAnalysis().get_daily_sales(sales_type=sales_type)
        return JsonResponse(sales)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_weekly_sales(request, sales_type):
    """Returns a JSON object containing the weekly sales data."""
    if request.method == 'GET':
        days = None
        if request.user.groups.filter(name='branches').exists():
            days = MainStorageAnalysis().get_weekly_sales(sales_type=sales_type, agent=request.user)
        else:
            days = MainStorageAnalysis().get_weekly_sales(sales_type=sales_type)
        return JsonResponse(days)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_sale_by_agent_monthly(request, sales_type):
    """Returns a JSON object containing the monthly sales data by agent."""
    if request.method == 'GET':
        sales_by_agent = None
        if request.user.groups.filter(name='branches').exists():
            sales_by_agent = MainStorageAnalysis().get_monthly_sales_by_agents(sales_type=sales_type, agent=request.user)
        else:
            sales_by_agent = MainStorageAnalysis().get_monthly_sales_by_agents(sales_type=sales_type)
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
                        sold=False, missing=False, assigned=True,
                        recieved=True, faulty=False, pending=False, issue=False))
                total += len(MainStorage.objects.filter(
                    agent=agent.user, in_stock=True,
                    sold=False, missing=False, assigned=True,
                    recieved=True, faulty=False, pending=False, issue=False))
        stocks['Total'] = total
        return JsonResponse(stocks)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_main_stock_analysis(request):
    """Returns a JSON object containing the main stock analysis."""
    if request.method == 'GET':
        main_shop_staff = Group.objects.get(name='main_shop')
        representatives = UserProfile.objects.filter(groups=main_shop_staff)
        data_set = MainStorage.objects.filter(
            agent__in=representatives, in_stock=True, sold=False,
            missing=False, assigned=True, recieved=True, faulty=False,
            pending=False, issue=False)
        stock = {}
        for item in data_set:
            stock[item.phone_type] = stock.get(item.phone_type, 0) + 1
        stock['Total'] = data_set.count()
        return JsonResponse(stock)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_individual_agent_stock(request):
    """Returns a JSON object containing the individual agent's stock."""
    if request.method == 'GET':
        agent = request.user
        stock = MainStorageAnalysis().get_agent_stock_in(agent)
        return JsonResponse(stock)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_individual_agent_stock_out(request):
    """Returns a JSON object containing the individual agent's stock."""
    if request.method == 'GET':
        agent = request.user
        stock = MainStorageAnalysis().get_agent_stock_out(agent)
        return JsonResponse(stock, safe=False)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_yearly_sales(request):
    """Returns a JSON object containing the yearly sales data."""
    if request.method == 'GET':
        sales = None
        if request.user.is_superuser:
            agent = UserProfile.objects.filter(groups__name='main_shop').first()
            sales = MainStorageAnalysis().get_sales_for_all_months(agent=agent)
        else:
            sales = MainStorageAnalysis().get_sales_for_all_months(request.user)
        return JsonResponse(sales, safe=False)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_yearly_sales_total(request):
    """Returns the total yearly sales."""
    if request.method == 'GET':
        sales = None
        if request.user.is_superuser:
            sales = MainStorageAnalysis().get_sales_for_all_months()
        else:
            sales = MainStorageAnalysis().get_sales_for_all_months(request.user)
        return JsonResponse(sales, safe=False)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def agent_daily_sales(request):
    """Returns a JSON object containing the daily sales data."""
    if request.method == 'GET':
        sales = AgentsDataQuery().daily_sales(request.user)
        return JsonResponse(sales)
    return JsonResponse({'error': 'Invalid request.'})

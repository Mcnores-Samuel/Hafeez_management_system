"""This model represent the entire stock available and sold in all posts."""
from ...models.main_storage import MainStorage
from ...models.agent_profile import AgentProfile
from django.utils import timezone


class MainStorageAnalysis:
    """This class contains methods for analyzing the MainStorage model."""
    def __init__(self, *args, **kwargs):
        pass

    def get_daily_sales(self, sales_type):
        """Returns a dictionary containing the daily sales data."""
        today = timezone.now().date()
        data_set = MainStorage.objects.filter(
            stock_out_date=today,
            sold=True, in_stock=False,
            sales_type=sales_type)
        sales = {}
        for data in data_set:
            sales[data.phone_type] = sales.get(data.phone_type, 0) + 1
        return sales
    
    def get_weekly_sales(self, sales_type):
        """Returns a dictionary containing the weekly sales data."""
        current_week = timezone.now().date()
        week_days = ['Monday', 'Tuesday', 'Wednesday',
                     'Thursday', 'Friday', 'Saturday',
                     'Sunday']
        days = {day: [] for day in week_days}
        monday = current_week - timezone.timedelta(
            days=current_week.weekday())
        sunday = monday + timezone.timedelta(days=6)

        data_set = MainStorage.objects.filter(
            stock_out_date__range=[monday, sunday],
            sold=True, in_stock=False,
            sales_type=sales_type)
        for data in data_set:
            item = {'type': data.phone_type}
            days[week_days[data.stock_out_date.weekday()]].append(item)
            item = {}
        return days
    
    def get_monthly_sales_by_agents(self, sales_type):
        """Returns a dictionary containing the monthly sales data."""
        agents = AgentProfile.objects.all().order_by('user__username')
        sales_by_agent = {}
        current_month = timezone.now().date().month
        current_year = timezone.now().date().year
        total_sales = MainStorage.objects.filter(
            stock_out_date__month=current_month,
            stock_out_date__year=current_year,
            sold=True, in_stock=False, sales_type=sales_type,
            missing=False)
        for agent in agents:
            sales_by_agent[str(agent.user.username).lower().capitalize()] = len(
                MainStorage.objects.filter(
                    agent=agent.user,
                    stock_out_date__month=current_month,
                    stock_out_date__year=current_year,
                    sold=True, in_stock=False, sales_type=sales_type,
                    missing=False))
        sales_by_agent['Total'] = len(total_sales)
        sales_by_agent = sorted(sales_by_agent.items(), key=lambda x: x[1], reverse=True)
        return sales_by_agent

"""This model represent the entire stock available and sold in all posts."""
from ...models.main_storage import MainStorage
from ...models.agent_profile import AgentProfile
from ...models.user_profile import UserProfile
from django.utils import timezone
from django.contrib.auth.models import Group



class MainStorageAnalysis:
    """This class contains methods for analyzing the MainStorage model."""
    def __init__(self, *args, **kwargs):
        pass

    def get_daily_sales(self, sales_type, agent=None, day=timezone.now().date()):
        """Returns a dictionary containing the daily sales data."""
        data_set = None
        if agent:
            data_set = MainStorage.objects.filter(
                agent=agent,
                stock_out_date=day,
                sold=True, in_stock=False,
                sales_type=sales_type)
        else:
            data_set = MainStorage.objects.filter(
                stock_out_date=day,
                sold=True, in_stock=False,
                sales_type=sales_type)
        sales = {}
        for data in data_set:
            sales[data.phone_type] = sales.get(data.phone_type, 0) + 1
        return sales
    
    def get_weekly_sales(self, sales_type, agent=None):
        """Returns a dictionary containing the weekly sales data."""
        current_week = timezone.now().date()
        week_days = ['Monday', 'Tuesday', 'Wednesday',
                     'Thursday', 'Friday', 'Saturday',
                     'Sunday']
        days = {day: [] for day in week_days}
        monday = current_week - timezone.timedelta(
            days=current_week.weekday())
        sunday = monday + timezone.timedelta(days=6)
        data_set = None
        if agent:
            data_set = MainStorage.objects.filter(
                agent=agent,
                stock_out_date__range=[monday, sunday],
                sold=True, in_stock=False,
                sales_type=sales_type)
        else:
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
            missing=False, pending=False, assigned=True,
            recieved=True, issue=False, faulty=False)
        for agent in agents:
            sales_by_agent[str(agent.user.username).lower().capitalize()] = MainStorage.objects.filter(
                    agent=agent.user,
                    stock_out_date__month=current_month,
                    stock_out_date__year=current_year,
                    sold=True, in_stock=False, sales_type=sales_type,
                    missing=False, pending=False, assigned=True,
                    recieved=True, issue=False, faulty=False).count()
        sales_by_agent['Total'] = total_sales.count()
        sales_by_agent = sorted(sales_by_agent.items(), key=lambda x: x[1], reverse=True)
        return sales_by_agent
    
    def get_agent_stock_in(self, agent):
        """Returns a dictionary containing the agent's stock in data."""
        stock_in = MainStorage.objects.filter(
            agent=agent,
            in_stock=True, assigned=True, available=True,
            missing=False, sold=False, pending=False,
            faulty=False, issue=False, recieved=True, paid=False)
        stock = {}
        for data in stock_in:
            stock[data.phone_type] = stock.get(data.phone_type, 0) + 1
        return stock
    
    def get_agent_stock_out(self, agent):
        """Returns a dictionary containing the agent's stock out data."""
        current_month = timezone.now().date().month
        current_year = timezone.now().date().year
        stock_out = MainStorage.objects.filter(
            agent=agent, in_stock=False,
            assigned=True, missing=False,
            sold=True, pending=False, faulty=False,
            stock_out_date__month=current_month,
            stock_out_date__year=current_year,
            recieved=True, issue=False)
        stock = {}
        for data in stock_out:
            stock[data.phone_type] = stock.get(data.phone_type, 0) + 1
        stock = sorted(stock.items(), key=lambda x: x[1], reverse=True)
        return stock
    
    def get_sales_for_all_months(self, agent):
        """Returns a dictionary containing the agent's sales for all months."""
        months = ['January', 'February', 'March', 'April', 'May',
                  'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        if agent.groups.filter(name='agents').exists():
            agent_profile = AgentProfile.objects.get(user=agent)
            if agent_profile:
                year = timezone.now().date().year
                sales = {}
                for month in months:
                    sales[month] = MainStorage.objects.filter(
                        agent=agent, in_stock=False,
                        assigned=True,
                        sold=True,
                        stock_out_date__month=months.index(month)+1,
                        stock_out_date__year=year,
                        pending=False, issue=False,
                        recieved=True, faulty=False).count()
                overall = 0 #placeholder
                return sales, overall
        elif (agent.groups.filter(name='staff_members').exists() or
              agent.is_superuser):
            sales = {}
            overall_sales = {}
            main_shop_staff = Group.objects.get(name='main_shop')
            representatives = UserProfile.objects.filter(groups=main_shop_staff)
            for month in months:
                total = MainStorage.objects.filter(
                    agent__in=representatives, in_stock=False,
                    assigned=True, sold=True, missing=False,
                    pending=False, stock_out_date__month=months.index(month)+1,
                    stock_out_date__year=timezone.now().date().year,
                    issue=False, recieved=True, faulty=False).count()
                main = MainStorage.objects.filter(in_stock=False,
                    assigned=True, sold=True, missing=False,
                    pending=False, stock_out_date__month=months.index(month)+1,
                    stock_out_date__year=timezone.now().date().year,
                    issue=False, recieved=True, faulty=False).count()
                sales[month] = total
                overall_sales[month] = main
            return sales, overall_sales
        return None
    
    def overall_stock(self, agent=None):
        """This function returns a JSON object containing
        the overall stock data.
        """
        if agent:
            stock = MainStorage.objects.filter(agent=agent, in_stock=True, assigned=True,
                sold=False, missing=False, pending=False, faulty=False, recieved=True, available=True,
                issue=False).count()
        else:
            stock = MainStorage.objects.filter( agent__groups__name__in=['agents', 'branches'], in_stock=True, assigned=True,
                    sold=False, missing=False, pending=False, faulty=False, recieved=True, available=True,
                    issue=False).count()

        return stock
    
    def overall_sales(self, agent=None):
        """This function returns a JSON object containing
        the overall sales data.
        """
        month = timezone.now().date().month
        year = timezone.now().date().year
        if agent:
            sales = MainStorage.objects.filter(agent=agent, in_stock=False, assigned=True,
                sold=True, missing=False, pending=False, faulty=False, stock_out_date__month=month,
                stock_out_date__year=year).count()
        else:
            sales = MainStorage.objects.filter(agent__groups__name__in=['agents', 'branches'], in_stock=False, assigned=True,
                    sold=True, missing=False, pending=False, faulty=False, stock_out_date__month=month,
                    stock_out_date__year=year).count()
        return sales
    
    def pending_sales(self, request):
        """This function returns a list of all pending sales.
        It also returns the total number of pending sales.
        """
        total_by_agents = {}
        all_agents = AgentProfile.objects.all().order_by('user__username')
        total = 0
        
        for agent in all_agents:
            data = MainStorage.objects.filter(
                agent=agent.user,
                pending=True, in_stock=False,
                assigned=True, sold=True, missing=False,
                faulty=False, issue=False).count()
            if data > 0:
                total_by_agents[agent.user.username] = data
            total += data

            sorted_data = sorted(total_by_agents.items(), key=lambda x: x[1], reverse=True)
        return sorted_data, total
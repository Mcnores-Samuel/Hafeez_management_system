"""This model represent the entire stock available and sold in all posts."""
from ...models.main_storage import MainStorage
from ...models.agent_profile import AgentProfile
from ...models.user_profile import UserProfile
from django.utils import timezone
from django.db.models import Count
from collections import defaultdict
import json


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
                sales_type=sales_type, agent__groups__name__in=["agents", "branches"])
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
                sales_type=sales_type,
                agent__groups__name__in=["agents", "branches"]).distinct()
        for data in data_set:
            item = {'type': data.phone_type}
            days[week_days[data.stock_out_date.weekday()]].append(item)
            item = {}
        return days
    
    def get_monthly_sales_by_agents(self, sales_type, agent=None):
        """Returns a dictionary containing the monthly sales data."""
        agents = None
        sales_by_agent = {}
        current_month = timezone.now().date().month
        current_year = timezone.now().date().year
        if agent:
            sales = MainStorage.objects.filter(
                agent=agent, stock_out_date__month=current_month,
                stock_out_date__year=current_year,
                sold=True, in_stock=False, sales_type=sales_type,
                missing=False, pending=False, assigned=True,
                recieved=True, issue=False, faulty=False)
            for sale in sales:
                sales_by_agent[sale.name] = sales_by_agent.get(sale.name, 0) + 1
            sales_by_agent['Total'] = sales.count()
            sales_by_agent = sorted(sales_by_agent.items(), key=lambda x: x[1], reverse=True)
        else:
            agents = UserProfile.objects.filter(groups__name__in=['agents', 'branches'])
            for agent in agents:
                total = MainStorage.objects.filter(
                    agent=agent,
                    stock_out_date__month=current_month,
                    stock_out_date__year=current_year,
                    sold=True, in_stock=False, sales_type=sales_type,
                    missing=False, pending=False, assigned=True,
                    recieved=True, issue=False, faulty=False).count()
                sales_by_agent[str(agent.username).lower().capitalize()] = total
                sales_by_agent['Total'] = sales_by_agent.get("Total", 0) + total
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

    def get_sales_for_all_months(self, agent=None):
        """Returns a dictionary containing the agent's sales for all months, categorized by year and agent,
        with an additional 'month_total' field."""
        
        months = ['January', 'February', 'March', 'April', 'May',
                'June', 'July', 'August', 'September', 'October',
                'November', 'December']
        
        current_year = timezone.now().year
        last_year = current_year - 1

        # Base query filters
        filters = {
            "in_stock": False,
            "assigned": True,
            "sold": True,
            "pending": False,
            "issue": False,
            "recieved": True,
            "faulty": False
        }
        
        if agent:
            filters["agent"] = agent
        else:
            filters["agent__groups__name__in"] = ['agents', 'branches']
            filters["missing"] = False

        # Query to fetch sales for both years, grouped by agent and month
        sales_data = (
            MainStorage.objects
            .filter(**filters, stock_out_date__year__in=[last_year, current_year])
            .values("stock_out_date__year", "stock_out_date__month", "agent__username")
            .annotate(sales_count=Count("id"))
        )

        # Organize data into the required format with month_total
        sales_summary = {
            "current_year": {month.lower(): defaultdict(int) for month in months},
            "last_year": {month.lower(): defaultdict(int) for month in months}
        }
        
        for entry in sales_data:
            year = entry["stock_out_date__year"]
            month = months[entry["stock_out_date__month"] - 1].lower()  # Convert to lowercase
            agent_name = entry["agent__username"]
            sales_count = entry["sales_count"]

            if year == last_year:
                sales_summary["last_year"][month][agent_name] = sales_count
            else:
                sales_summary["current_year"][month][agent_name] = sales_count

        # Calculate month_total for each month
        for year_key in ["current_year", "last_year"]:
            for month in sales_summary[year_key]:
                sales_summary[year_key][month]["month_total"] = sum(
                    sales_summary[year_key][month].values()
                )
        return sales_summary
    
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
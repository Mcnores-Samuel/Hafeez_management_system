"""This module contains methods for querying the database
for data to be used by the agents app.
"""
from ...models.main_storage import MainStorage
from ...models.agent_profile import AgentProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q


class AgentsDataQuery:
    """This class contains methods for querying the database
    for data to be used by the agents app.
    """
    def __init__(self, *args, **kwargs):
        pass

    def daily_sales(self, user):
        """Returns the daily sales for the agent."""
        if user.groups.filter(name='agents').exists():
            agent_profile = AgentProfile.objects.get(user=user)
            if agent_profile:
                daily_sales = MainStorage.objects.filter(
                    agent=user, stock_out_date=timezone.now().date(),
                    in_stock=False, assigned=True, sold=True,
                    missing=False, pending=False, issue=False,
                    faulty=False)
                sales = {}
                for sale in daily_sales:
                    sales[sale.phone_type] = sales.get(sale.phone_type, 0) + 1
                return sales
        return None

    def stock(self, user, status, request, month=timezone.now().date().month,
              year=timezone.now().date().year):
        """Returns a list of devices in stock."""
        data = None
        if user and status == True:
            data = MainStorage.objects.filter(
                agent=user, in_stock=True,
                assigned=True, missing=False,
                pending=False, issue=False, sold=False,
                recieved=True, faulty=False,
                paid=False).all().order_by('-entry_date')
        elif user and status == False:
            data = MainStorage.objects.filter(
                agent=user, in_stock=False,
                assigned=True, missing=False,
                stock_out_date__month=month,
                stock_out_date__year=year,
                pending=False, sold=True, issue=False,
                faulty=False).all().order_by('-stock_out_date')
            
        total = data.count()
        paginator = Paginator(data, 12)
        page_number = request.GET.get('page')

        try:
            data = paginator.page(page_number)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        return data, total

    def search(self, user, search_term, request, status, sold):
        """Returns a list of devices matching the search term."""
        if user.is_authenticated:
            queryset = MainStorage.objects.filter(
                Q(device_imei__icontains=search_term) |
                Q(device_imei_2__icontains=search_term) |
                Q(name__icontains=search_term) |
                Q(phone_type__icontains=search_term) |
                Q(contract_no__icontains=search_term) |
                Q(category__icontains=search_term) |
                Q(sales_type__icontains=search_term)
            ).filter(agent=user, in_stock=status,
                    assigned=True, missing=False, sold=sold).all().order_by('-entry_date')
            total = queryset.count()
            paginator = Paginator(queryset, 12)
            page_number = request.GET.get('page')

            try:
                paginated_queryset = paginator.page(page_number)
            except PageNotAnInteger:
                paginated_queryset = paginator.page(1)
            except EmptyPage:
                paginated_queryset = paginator.page(paginator.num_pages)
            return paginated_queryset, total
        return None
    
    def search_stock_out(self, user, search_term, request):
        """Returns a list of devices matching the search term.
        This method is used to search for devices that have been sold.

        Args:
            user (User): The user object.
            search_term (str): The search term.
            request (HttpRequest): The request object.

        Returns:
            QuerySet: A queryset containing the search results.
        """
        if user.is_authenticated:
            queryset = MainStorage.objects.filter(
                Q(device_imei__icontains=search_term) |
                Q(device_imei_2__icontains=search_term) |
                Q(name__icontains=search_term) |
                Q(phone_type__icontains=search_term) |
                Q(contract_no__icontains=search_term) |
                Q(category__icontains=search_term) |
                Q(sales_type__icontains=search_term)
            ).filter(agent=user, in_stock=False,
                        assigned=True, missing=False,
                        sold=True).all().order_by('-stock_out_date')
            total = queryset.count()
            paginator = Paginator(queryset, 12)
            page_number = request.GET.get('page')

            try:
                paginated_queryset = paginator.page(page_number)
            except PageNotAnInteger:
                paginated_queryset = paginator.page(1)
            except EmptyPage:
                paginated_queryset = paginator.page(paginator.num_pages)
            return paginated_queryset, total
        return None

                
    def sale_on_credit(self, user, item_id):
        """Returns a list of devices sold on credit."""
        if user.groups.filter(name='agents').exists():
            agent_profile = AgentProfile.objects.get(user=user)
            if agent_profile:
                item = MainStorage.objects.get(id=item_id)
                if item:
                    item.pending = True
                    item.in_stock = False
                    item.sold = True
                    item.sales_type = 'Loan'
                    item.stock_out_date = timezone.now().date()
                    item.save()
                    return item
                
    def pending_sales(self, user, request):
        """Returns a list of pending sales."""
        if user.groups.filter(name='agents').exists():
            agent_profile = AgentProfile.objects.get(user=user)
            if agent_profile:
                all_pending_sales = MainStorage.objects.filter(
                    agent=user,
                    pending=True, in_stock=False,
                    assigned=True, sold=True, missing=False,
                    faulty=False, issue=False).order_by('stock_out_date')
                total_pending_sales = all_pending_sales.count()
                paginator = Paginator(all_pending_sales, 12)
                page = request.GET.get('page')

                try:
                    all_pending_sales = paginator.get_page(page)
                except PageNotAnInteger:
                    all_pending_sales = paginator.page(1)
                except EmptyPage:
                    all_pending_sales = paginator.page(paginator.num_pages)
                return all_pending_sales, total_pending_sales
        return None
    
    def agent_new_stock(self, user, request):
        """Returns a list of new stock."""
        if user.groups.filter(name='agents').exists():
            agent_profile = AgentProfile.objects.get(user=user)
            if agent_profile:
                new_stock = MainStorage.objects.filter(
                    agent=user, recieved=False).all().order_by('-entry_date')
                paginator = Paginator(new_stock, 12)
                page_number = request.GET.get('page')

                try:
                    new_stock = paginator.page(page_number)
                except PageNotAnInteger:
                    new_stock = paginator.page(1)
                except EmptyPage:
                    new_stock = paginator.page(paginator.num_pages)
                return new_stock
        return None
    
    def agent_issues(self, user, request):
        """Returns a list of issues reported by the agent."""
        if user.groups.filter(name='agents').exists():
            agent_profile = AgentProfile.objects.get(user=user)
            if agent_profile:
                all_issues = MainStorage.objects.filter(
                    agent=user, issue=True).order_by('stock_out_date')
                paginator = Paginator(all_issues, 12)
                page = request.GET.get('page')

                try:
                    all_issues = paginator.get_page(page)
                except PageNotAnInteger:
                    all_issues = paginator.page(1)
                except EmptyPage:
                    all_issues = paginator.page(paginator.num_pages)
                return all_issues
        return None
    
    def agent_faults(self, user, request):
        """Returns a list of faulty devices."""
        if user.groups.filter(name='agents').exists():
            agent_profile = AgentProfile.objects.get(user=user)
            if agent_profile:
                all_faults = MainStorage.objects.filter(
                    agent=user, faulty=True).order_by('stock_out_date')
                paginator = Paginator(all_faults, 12)
                page = request.GET.get('page')

                try:
                    all_faults = paginator.get_page(page)
                except PageNotAnInteger:
                    all_faults = paginator.page(1)
                except EmptyPage:
                    all_faults = paginator.page(paginator.num_pages)
                return all_faults
        return None
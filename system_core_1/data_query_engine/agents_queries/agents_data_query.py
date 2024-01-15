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

    def stock(self, user, status, request):
        """Returns a list of devices in stock."""
        if user.groups.filter(name='agents').exists():
            agent_profile = AgentProfile.objects.get(user=user)
            if agent_profile and status:
                stock_in = MainStorage.objects.filter(
                    agent=user, in_stock=True,
                    assigned=True,
                    missing=False).all().order_by('-entry_date')
                paginator = Paginator(stock_in, 12)
                page_number = request.GET.get('page')

                try:
                    stock_in = paginator.page(page_number)
                except PageNotAnInteger:
                    stock_in = paginator.page(1)
                except EmptyPage:
                    stock_in = paginator.page(paginator.num_pages)
                return stock_in
            elif agent_profile and not status:
                current_month = timezone.now().date().month
                current_year = timezone.now().date().year
                stock_out = MainStorage.objects.filter(
                    agent=user, in_stock=False,
                    assigned=True, missing=False,
                    stock_out_date__month=current_month,
                    stock_out_date__year=current_year).all().order_by('-stock_out_date')
                paginator = Paginator(stock_out, 12)
                page_number = request.GET.get('page')

                try:
                    stock_out = paginator.page(page_number)
                except PageNotAnInteger:
                    stock_out = paginator.page(1)
                except EmptyPage:
                    stock_out = paginator.page(paginator.num_pages)
                return stock_out
        return None
            
    def search(self, user, search_term, queryset, request):
        """Returns a list of devices matching the search term."""
        if user.groups.filter(name='agents').exists():
            agent_profile = AgentProfile.objects.get(user=user)
            if agent_profile:
                search_term = search_term.lower()
                queryset = queryset.filter(
                    Q(device_imei__icontains=search_term) |
                    Q(name__icontains=search_term) |
                    Q(phone_type__icontains=search_term)
                ).order_by('-entry_date')

                paginator = Paginator(queryset, 12)
                page_number = request.GET.get('page')

                try:
                    queryset = paginator.page(page_number)
                except PageNotAnInteger:
                    queryset = paginator.page(1)
                except EmptyPage:
                    queryset = paginator.page(paginator.num_pages)
                return queryset
        return None
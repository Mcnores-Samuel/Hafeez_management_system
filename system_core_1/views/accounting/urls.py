from django.urls import path
from system_core_1.views.accounting.revenue import (
    current_year_revenue, revenue_by_category, calculateCreditRevenue,
    lastyearBycurrentMonth, revenue_growth, average_order_value, calculateCashRevenue
)
from system_core_1.views.accounting.accounting import getCostAndRevenue, accounting
from system_core_1.views.expenses import expenses


urlpatterns = [
    path('expenses/', expenses, name='expenses'),
    path('accounting/', accounting, name='accounting'),
    path('calculateCreditRevenue/', calculateCreditRevenue, name='calculateCreditRevenue'),
    path('calculateCashRevenue/', calculateCashRevenue, name='calculateCashRevenue'),
    path('getCostAndRevenue/', getCostAndRevenue, name='getCostAndRevenue'),
    path('current_year_revenue/', current_year_revenue, name='current_year_revenue'),
    path('revenue_by_category/', revenue_by_category, name='revenue_by_category'),
    path('lastyearBycurrentMonth/', lastyearBycurrentMonth, name='lastyearBycurrentMonth'),
    path('revenue_growth/', revenue_growth, name='revenue_growth'),
    path('average_order_value/', average_order_value, name='average_order_value'),
]
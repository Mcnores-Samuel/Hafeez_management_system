from django.urls import path
from system_core_1.views.analytics import data_for_charts
from system_core_1.views.analytics import stock_analysis

urlpatterns = [
    # data analysis urls
    path('get_daily_sales/<str:sales_type>/', data_for_charts.get_daily_sales, name='get_daily_sales'),
    path('get_weekly_sales/<str:sales_type>/', data_for_charts.get_weekly_sales, name='get_weekly_sales'),
    path('get_sale_by_agent_monthly/<str:sales_type>/', data_for_charts.get_sale_by_agent_monthly, name='get_sale_by_agent_monthly'),
    path('get_individual_agent_stock/', data_for_charts.get_individual_agent_stock, name='get_individual_agent_stock'),
    path('get_individual_agent_stock_out/', data_for_charts.get_individual_agent_stock_out, name='get_individual_agent_stock_out'),
    path('get_agents_stock_json/', data_for_charts.get_agents_stock_json, name='get_agents_stock_json'),
    path('get_yearly_sales/', data_for_charts.get_yearly_sales, name='get_yearly_sales'),
    path('get_yearly_sales_total/', data_for_charts.get_yearly_sales_total, name='get_yearly_sales_total'),
    path('agent_daily_sales/', data_for_charts.agent_daily_sales, name='agent_daily_sales'),
    path('get_main_stock_analysis/', data_for_charts.get_main_stock_analysis, name='get_main_stock_analysis'),
    path('get_source_stock/', stock_analysis.get_source_stock, name='get_source_stock'),
    path('get_yearly_product_sales/', stock_analysis.get_yearly_product_sales, name='get_yearly_product_sales'),
    path('admin_stock_analysis/', stock_analysis.admin_stock_analysis, name='admin_stock_analysis'),
]
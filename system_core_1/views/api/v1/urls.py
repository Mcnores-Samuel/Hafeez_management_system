from django.urls import path
from system_core_1.views.api.v1 import sales_update_api

urlpatterns = [
    path('stockQuery/', sales_update_api.stockQuery, name='stockQuery'),
    path('salesUpdates/', sales_update_api.salesUpdates, name='salesUpdates'),
    path('updateTimeStamp/', sales_update_api.updateTimeStamp, name='updateTimeStamp'),
    path('pendingSales/', sales_update_api.pendingSales, name='pendingSales'),
    path('partners_stockQuery/', sales_update_api.partners_stockQuery, name='partners_stockQuery'),
    path('partner_invoices/<str:partner_username>/', sales_update_api.partner_invoices, name='partner_invoices'),
    path('airtel_sales_data/', sales_update_api.airtel_sales_data, name='airtel_sales_data'),
]
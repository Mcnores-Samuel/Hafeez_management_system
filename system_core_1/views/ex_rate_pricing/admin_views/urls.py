from django.urls import path
from system_core_1.views.ex_rate_pricing.admin_views.entry import (
    ex_rate_pricing, data_per_partner, add_exchange_rate, get_exchange_rate, get_outstanding_invoice
)
from system_core_1.views.ex_rate_pricing.admin_views.update import (
    update_cost_by_rate, invoice_paid
)

urlpatterns = [
    path('ex_rate_pricing/', ex_rate_pricing, name='ex_rate_pricing'),
    path('data_per_partner/', data_per_partner, name='data_per_partner'),
    path('add_exchange_rate/', add_exchange_rate, name='add_exchange_rate'),
    path('get_exchange_rate/', get_exchange_rate, name='get_exchange_rate'),
    path('get_outstanding_invoice/', get_outstanding_invoice, name='get_outstanding_invoice'),
    path('update_cost_by_rate/', update_cost_by_rate, name='update_cost_by_rate'),
    path('invoice_paid/<int:invoice_id>/', invoice_paid, name='invoice_paid'),
]
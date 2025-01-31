"""This model represent the cost per invoice in the system."""
from django.contrib import admin



class CostPerInvoiceAdmin(admin.ModelAdmin):
    """The `CostPerInvoiceAdmin` class is used to customize the
    admin interface for the CostPerInvoice model.
    """
    list_display = ('partner', 'invoice_number', 'invoice_date', 'total_invoice_items', 'original_cost',
                    'cost_per_ex_rate', 'total_items_sold', 'created_at', 'updated_at', 'is_paid', 'date_paid',
                    'last_payment_amount', 'last_payment_date', 'last_payment_method', 'current_balance',
                    'total_amount_paid')
    search_fields = ('invoice_number', 'invoice_date', 'total_invoice_items', 'original_cost',
                     'cost_per_ex_rate', 'total_items_sold', 'created_at', 'updated_at', 'is_paid', 'date_paid',
                     'last_payment_amount', 'last_payment_date', 'last_payment_method', 'current_balance',
                     'total_amount_paid')
    


class DailyExchangeRateAdmin(admin.ModelAdmin):
    """The `DailyExchangeRateAdmin` class is used to customize the
    admin interface for the DailyExchangeRate model.
    """
    list_display = ('date', 'exchange_rate', 'valid')
    list_filter = ('date', 'valid')
    search_fields = ('date', 'exchange_rate')

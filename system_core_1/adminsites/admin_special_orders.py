"""This module contains the special orders admin class."""
from django.contrib import admin


class SpecialOrdersAdmin(admin.ModelAdmin):
    """This class contains the special orders admin."""
    list_display = ('presentative', 'current_orders', 'last_payments',
                    'initial_balances', 'new_balance', 'final_balances',
                    'total_paid', 'month', 'year', 'current_payment',
                    'last_payment_date', 'created_on', 'updated_on')
    search_fields = ('presentative', 'created_on', 'updated_on',
                     'current_orders', 'initial_balance', 'current_balance',
                     'final_balance')
    
    list_filter = ('created_on', 'updated_on')

    list_per_page = 20

    actions = ['calculate_balances']

    def last_payments(self, obj):
        return f"{obj.last_payment:,}".replace(',', ', ')

    def new_balance(self, obj):
        return f"{obj.current_balance:,}".replace(',', ', ')
    
    def initial_balances(self, obj):
        return f"{obj.initial_balance:,}".replace(',', ', ')
    
    def final_balances(self, obj):
        return f"{obj.final_balance:,}".replace(',', ', ')
    
    def total_paid(self, obj):
        return f"{obj.total_paid:,}".replace(',', ', ')
    
    def current_payment(self, obj):
        return f"{obj.current_payment:,}".replace(',', ', ')
    
    def calculate_balances(self, request, queryset):
        """Calculate the balances for the special orders"""
        for obj in queryset:
            if obj:
                obj.final_balance = obj.initial_balance + obj.current_balance
                obj.initial_balance = obj.final_balance
                obj.save()
    calculate_balances.short_description = "Calculate balances"
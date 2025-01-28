"""This module contains the admin site configuration for the expenses table."""
from django.contrib import admin


class ExpensesAdmin(admin.ModelAdmin):
    """The admin configuration for the expenses table."""
    list_display = ('user', 'amount', 'description', 'category', 'date')
    list_filter = ('user', 'date', 'category')
    search_fields = ('user__first_name', 'user__last_name', 'description')
    ordering = ('-date',)
    list_per_page = 50


class FixedAssetsAdmin(admin.ModelAdmin):
    """The admin configuration for the fixed assets table."""
    list_display = ('name', 'description', 'date_purchased', 'cost',
                    'useful_life', 'salvage_value', 'depreciation')
    search_fields = ('name', 'description')
    list_per_page = 50


class CapitalAdmin(admin.ModelAdmin):
    """The admin configuration for the categories table."""
    list_display = ('source', 'amount', 'description', 'date')
    list_filter = ('source', 'date')
    search_fields = ('source', 'description')
    ordering = ('-date',)
    list_per_page = 50


class LiabilityAdmin(admin.ModelAdmin):
    """The admin configuration for the liabilities table."""
    list_display = ('creditor', 'type', 'amount', 'description', 'effective_date',
                    'due_date', 'interest_rate', 'is_paid', 'date_paid')
    list_filter = ('creditor', 'type', 'effective_date', 'due_date', 'is_paid')
    search_fields = ('creditor', 'type', 'description')
    ordering = ('-effective_date',)
    list_per_page = 50
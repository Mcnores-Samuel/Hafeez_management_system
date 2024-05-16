"""This module contains the model for the final sales table in the database."""
from ..models.account_manager import AccountManager
from django.contrib import admin


class AccountManagerAdmin(admin.ModelAdmin):
    """AccountManager admin class for the admin panel."""
    list_display = ('mbo', 'contract', 'device_imei', 'device_name', 'date_created',
                    'date_updated', 'active', 'approved', 'rejected', 'issue')
    search_fields = ('mbo__user__username', 'contract', 'device_imei', 'device_name')
    list_filter = ('active', 'approved', 'rejected', 'issue', 'mbo')
    list_per_page = 20


"""This module contains the model for the final sales table in the database."""
from ..models.account_manager import AccountManager
from django.contrib import admin


class AccountManagerAdmin(admin.ModelAdmin):
    """AccountManager admin class for the admin panel."""
    list_display = ('mbo', 'contract', 'date_created',
                    'date_updated', 'active', 'approved', 'rejected', 'issue')
    search_fields = ('mbo__user__username', 'contract')
    list_per_page = 20


"""This module contains the admin commission panel view,
which is used to display the commission panel
"""
from django.contrib import admin


class CommissionAdmin(admin.ModelAdmin):
    """This model represent the entire stock available and sold in all posts"""
    list_display = ('agent', 'total_devices_sold', 'amount', 'target',
                    'month', 'year', 'paid'
                    )

    search_fields = ('agent__username', 'month', 'year')

    list_filter = ('month', 'year', 'paid')

    list_per_page = 50

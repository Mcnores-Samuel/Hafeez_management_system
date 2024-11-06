"""This module contains the admin configuration for the PromoterPayments model."""
from django.contrib import admin
from ..customfilters.agent_filter import AirtelAgentFilter


class PromoterPaymentsAdmin(admin.ModelAdmin):
    """PromoterPayments admin class for the admin panel."""
    list_display = ('promoter', 'amount_paid', 'total_mifi_paid', 'total_idu_paid', 'total_devices_paid', 'payment_date', 'updated_by')
    search_fields = ('promoter__user__username', 'amount_paid', 'total_mifi_paid', 'total_idu_paid')
    list_filter = ('payment_date', AirtelAgentFilter)
    list_per_page = 50
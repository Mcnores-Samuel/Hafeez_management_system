from django.contrib import admin
from ..customfilters.agent_filter import AirtelAgentFilter


class Airtel_mifi_storageAdmin(admin.ModelAdmin):
    """This model represent the entire stock available and sold in all posts"""
    list_display = ('promoter', 'device_imei', 'device_type', 'in_stock',
                    'device_phone_no', 'days_left', 'team_leader', 'entry_date',
                    'collected_on', 'last_updated', 'next_due_date', 'date_sold',
                    'actived', 'payment_confirmed', 'returned', 'returned_by',
                    'returned_on', 'cash_recieved_by', 'paid', 'updated_by')

    search_fields = ('device_imei', 'device_type', 'entry_date',
                     'date_sold', 'agent__username', 'cash_recieved_by')

    list_filter = ('in_stock', 'device_type', AirtelAgentFilter, 'paid',
                   'entry_date', 'collected_on', 'date_sold', 'actived',
                   'payment_confirmed', 'returned', 'returned_by')

    list_per_page = 50

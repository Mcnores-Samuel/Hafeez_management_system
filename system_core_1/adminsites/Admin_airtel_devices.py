from django.contrib import admin
from ..customfilters.agent_filter import AirtelAgentFilter


class Airtel_mifi_storageAdmin(admin.ModelAdmin):
    """This model represent the entire stock available and sold in all posts"""
    list_display = ('assigned_to', 'recieved', 'device_imei', 'phone_number', 'device',
                    'pending', 'active', 'inactive', 'in_stock',
                    'assigned', 'entry_date', 'stock_out_date', 'collected_on',
                    'cash_recieved', 'cash_recieved_by', 'paid', 'comment'
                    )

    search_fields = ('device_imei', 'device', 'entry_date',
                     'stock_out_date', 'agent__username', 'cash_recieved_by')

    list_filter = ('in_stock', 'device', 'assigned', AirtelAgentFilter, 'paid',
                   'entry_date', 'collected_on', 'stock_out_date', 'active', 'inactive')

    list_per_page = 50

    def assigned_to(self, obj):
        """Return the agent to whom the phone is assigned"""
        return obj.agent

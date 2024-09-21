from django.contrib import admin
from ..customfilters.agent_filter import AirtelAgentFilter


class Airtel_mifi_storageAdmin(admin.ModelAdmin):
    """This model represent the entire stock available and sold in all posts"""
    list_display = ('promoter', 'device_imei', 'device_type', 'in_stock',
                    'device_phone_no', 'days_left', 'team_leader', 'entry_timestamp',
                    'collected_timestamp', 'last_updated_timestamp', 'next_due_date_timestamp', 'date_sold_timestamp',
                    'activated', 'payment_confirmed', 'returned', 'returned_by',
                    'returned_on_timestamp', 'cash_recieved_by', 'paid', 'updated_by')

    search_fields = ('device_imei', 'device_type', 'entry_date',
                     'date_sold', 'promoter__username', 'cash_recieved_by')

    list_filter = ('in_stock', 'device_type', AirtelAgentFilter, 'paid',
                   'entry_date', 'collected_on', 'date_sold', 'activated',
                   'payment_confirmed', 'returned', 'returned_by')

    list_per_page = 50

    def entry_timestamp(self, obj):
        """Return the timestamp of the entry date"""
        return obj.entry_date
    
    def collected_timestamp(self, obj):
        """Return the timestamp of the collection date"""
        return obj.collected_on
    
    def last_updated_timestamp(self, obj):
        """Return the timestamp of the last update"""
        return obj.last_updated
    
    def next_due_date_timestamp(self, obj):
        """Return the timestamp of the next due date"""
        return obj.next_due_date
    
    def date_sold_timestamp(self, obj):
        """Return the timestamp of the date sold"""
        return obj.date_sold
    
    def returned_on_timestamp(self, obj):
        """Return the timestamp of the date returned"""
        return obj.returned_on

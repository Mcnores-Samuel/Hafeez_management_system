from django.contrib import admin
from system_core_1.customfilters.agent_filter import AirtelAgentFilter
from django.utils import timezone


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

    actions = ['mark_as_sold', 'mark_as_returned', 'mark_as_not_in_stock']

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

    def not_in_stock(self, request, queryset):
        for obj in queryset:
            if obj:
                obj.in_stock = False
                obj.save()
    not_in_stock.short_description = "Mark as not in stock"

    def mark_as_sold(self, request, queryset):
        """Mark the phone as sold"""
        for obj in queryset:
            if obj:
                obj.in_stock = False
                obj.activated = True
                obj.payment_confirmed = True
                obj.paid = True
                obj.date_sold = timezone.now().date()
                obj.save()
    mark_as_sold.short_description = "Mark as sold"

    def mark_as_returned(self, request, queryset):
        """Mark the phone as returned"""
        for obj in queryset:
            if obj:
                obj.returned = True
                obj.returned_on = timezone.now().date()
                obj.save()
    mark_as_returned.short_description = "Mark as returned"

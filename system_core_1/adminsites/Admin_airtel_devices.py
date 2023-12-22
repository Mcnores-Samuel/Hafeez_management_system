from django.contrib import admin


class Airtel_mifi_storageAdmin(admin.ModelAdmin):
    """This model represent the entire stock available and sold in all posts"""
    list_display = ('assigned_to', 'recieved', 'device_imei', 'phone_number', 'secondary_phone_number', 'device',
                    'pending', 'active', 'inactive', 'in_stock',
                    'assigned', 'entry_date', 'stock_out_date', 'collected_on',
                    'cash_recieved', 'paid', 'image', 'comment'
                    )
    
    search_fields = ('device_imei', 'device', 'entry_date',
                     'stock_out_date', 'agent__username')
    
    list_filter = ('in_stock', 'device', 'assigned', 'paid',
                     'entry_date', 'collected_on', 'stock_out_date', 'agent__username')
    
    list_per_page = 50

    def assigned_to(self, obj):
        """Return the agent to whom the phone is assigned"""
        return obj.agent
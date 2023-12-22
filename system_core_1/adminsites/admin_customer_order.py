"""This module registers the PhoneData model with the admin site."""
from django.contrib import admin

class PhoneDataAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'agent_name', 'phone_name',
                    'imei_number', "contract_number", 'selling_price',
                    'cost_price', 'deposit', 'payment_period')
    search_fields = ('customer__customer_name', 'agent__user__username',
                     'phone_type', 'imei_number', 'contract_number')
    
    list_per_page = 20

    def customer_name(self, obj):
        return obj.customer.customer_name
    
    def agent_name(self, obj):
        return obj.agent.user.username

    def phone_name(self, obj):
        return obj.phone_type
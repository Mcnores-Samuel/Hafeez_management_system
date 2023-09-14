from django.contrib import admin
from .models import *
from .forms import AgentStockForm
from django.contrib.auth.admin import UserAdmin


admin.site.site_header = "HAFEEZ MANAGEMENT SYSTEM"
admin.site.site_title = "Hafeez"

@admin.register(UserProfile)
class UserAdminModel(UserAdmin):
    list_display = (
        'email', 'username', 'first_name', 'last_name',
        'phone_number', 'is_staff', 'is_active', 'date_joined',
        'last_login'
    )

@admin.register(MainStorage)
class MainStorageData(admin.ModelAdmin):
    list_display = (
        'device_imei', 'phone_type', 'in_stock',
        'sales_type', 'contract_no', 'entry_date',
        'stock_out_date', 'assigned'
    )
    list_filter = ('in_stock', 'entry_date')
    search_fields = ('device_imei', 'phone_type')


@admin.register(phone_reference)
class PhoneReferenceAdmin(admin.ModelAdmin):
    list_display = ("phone", "initial_deposit", "merchant")

    def initial_deposit(self, obj):
        return f"{obj.deposit:,}"
    
    def merchant(self, obj):
        return f"{obj.merchant_price:,}"


@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_agent')


@admin.register(AgentStock)
class AgentStockAdmin(admin.ModelAdmin):
    list_display = ('agent', 'device_imei', 'phone_type', 'sales_type', 'contract_number',
                     'collection_date', 'in_stock', 'stock_out_date')
    list_filter = ('in_stock', 'collection_date')
    search_fields = ('imei_number', 'phone_type', 'assigned')

    def device_imei(self, obj):
        return obj.imei_number
    
    form = AgentStockForm

    def save_model(self, request, obj, form, change):
        """Update MainStorage when assigning a phone to an agent"""
        if obj.in_stock and obj.agent:
            try:
                main_storage_phone = MainStorage.objects.get(device_imei=obj.imei_number, in_stock=True)
                main_storage_phone.assigned = True
                main_storage_phone.save()
            except MainStorage.DoesNotExist:
                pass
        super().save_model(request, obj, form, change)

    def delete_selected(self, request, queryset):
        """Unassign the phone from an agent in MainStorage when it's deleted"""
        for obj in queryset:
            if obj:
                try:
                    main_storage_phone = MainStorage.objects.get(device_imei=obj.imei_number, in_stock=True)
                    main_storage_phone.assigned = False
                    main_storage_phone.in_stock = True
                    main_storage_phone.save()

                except MainStorage.DoesNotExist:
                    main_storage_phone = MainStorage.objects.get(device_imei=obj.imei_number, in_stock=False, assigned=True)
                    main_storage_phone.assigned = False
                    main_storage_phone.in_stock = True
                    main_storage_phone.sales_type = '##'
                    main_storage_phone.stock_out_date = main_storage_phone.entry_date
                    main_storage_phone.save()
                except MainStorage.DoesNotExist:
                    pass
            obj.delete()
    actions = [delete_selected]


@admin.register(CustomerData)
class CustomerDataAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "national_id", "customer_contact", "second_contact", "customer_email",
                    "first_witness_name", "first_witness_contact", "second_witness_name", "second_witness_contact",
                    "customer_location", "nearest_school", "nearest_market_church_hospital", "created_at")
    

@admin.register(PhoneData)
class PhoneDataAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'agent', 'phone_name', 'imei_number', "contract_number", 'selling_price',
                    'cost_price', 'deposit', 'payment_period')
    
    def customer_name(self, obj):
        return obj.customer.customer_name
    
    def phone_name(self, obj):
        return obj.phone_type

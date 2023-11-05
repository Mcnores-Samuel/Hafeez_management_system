from django.contrib import admin
from .models.customer_details import CustomerData
from .models.agent_profile import AgentProfile
from .models.customer_order import PhoneData
from .models.user_profile import UserProfile, UserAvatar
from .models.main_storage import MainStorage
from .models.reference import Phone_reference
from .models.agent_stock import AgentStock
from django.contrib.auth.admin import UserAdmin
from .models.user_profile import Employee


admin.site.site_header = "HAFEEZ MANAGEMENT SYSTEM"
admin.site.site_title = "Hafeez"
admin.site.index_title = "Welcome to Hafeez Management System"


@admin.register(UserProfile)
class UserAdminModel(UserAdmin):
    list_display = (
        'email', 'username', 'first_name', 'last_name',
        'phone_number', 'is_staff', 'is_active', 'date_joined',
        'last_login'
    )


@admin.register(MainStorage)
class MainStorageData(admin.ModelAdmin):
    list_display = ('agent', 'recieved', 'device_imei', 'category', 'name', 'phone_type',
                    'spec', 'screen_size', 'os', 'battery', 'camera', 'in_stock',
                    'sales_type', 'contract_no', 'entry_date', 'stock_out_date',
                    'assigned', 'sold', 'paid', 'image'
    )
    search_fields = ('device_imei', 'phone_type', 'entry_date', 'category', 'agent__username')

    actions = ['update_images', 'verify_stock_recieved',
               'unverify_stock_recieved', 'unassign_select']

    def update_images(self, request, queryset):
        # Get the image from the first selected object
        image = queryset.first().image

        for phone in queryset:
            phone.image = image
            phone.save()

    update_images.short_description = "Update selected phones with the same image"

    def verify_stock_recieved(self, request, queryset):
        """Verify stock recieved by the agent"""
        for obj in queryset:
            if obj:
                obj.recieved = True
                obj.save()
    verify_stock_recieved.short_description = "Verify stock recieved"

    def unverify_stock_recieved(self, request, queryset):
        """Unverify stock recieved by the agent"""
        for obj in queryset:
            if obj:
                obj.recieved = False
                obj.save()
    unverify_stock_recieved.short_description = "Unverify stock recieved"

    def unassign_select(self, request, queryset):
        """Unassign the phone from an agent in MainStorage when requested"""
        for obj in queryset:
            try:
                device = MainStorage.objects.get(device_imei=obj.device_imei, in_stock=True,
                                                 assigned=True)
                device.agent = None
                device.recieved = False
                device.assigned = False
                device.in_stock = True
                device.sold = False
                device.contract_no = '##'
                device.sales_type = '##'
                device.stock_out_date = device.entry_date
                device.save()
            except MainStorage.DoesNotExist:
                pass
    unassign_select.short_description = "Unassign selected phones"


@admin.register(Phone_reference)
class PhoneReferenceAdmin(admin.ModelAdmin):
    list_display = ("phone", "initial_deposit", "merchant", 'cash')

    def initial_deposit(self, obj):
        return f"MK{obj.deposit:,}".replace(',', ' ')
    
    def merchant(self, obj):
        return f"MK{obj.merchant_price:,}".replace(',', ' ')
    
    def cash(self, obj):
        return f"MK{obj.cash_price:,}".replace(',', ' ')


@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_agent', 'contact_number',
                    'location', 'longitude', 'latitude')


@admin.register(AgentStock)
class AgentStockAdmin(admin.ModelAdmin):
    list_display = ('agent_name', 'device_imei', 'phone_type', 'sales_type', 'collection_date', 'in_stock',
                    'stock_out_date', 'contract_number')
    list_filter = ('in_stock', 'collection_date')
    search_fields = ('imei_number', 'phone_type', 'agent__user__username')

    def device_imei(self, obj):
        return obj.imei_number
    
    def agent_name(self, obj):
        return obj.agent.user.username

    def delete_selected(self, request, queryset):
        """Unassign the phone from an agent in MainStorage when it's deleted"""
        for obj in queryset:
            if obj:
                try:
                    main_storage_phone = MainStorage.objects.get(
                        device_imei=obj.imei_number, in_stock=True)
                    main_storage_phone.assigned = False
                    main_storage_phone.in_stock = True
                    main_storage_phone.sold = False
                    main_storage_phone.contract_no = '##'
                    main_storage_phone.sales_type = '##'
                    main_storage_phone.stock_out_date = main_storage_phone.entry_date
                    main_storage_phone.save()

                except MainStorage.DoesNotExist:
                    main_storage_phone = MainStorage.objects.get(
                        device_imei=obj.imei_number, in_stock=False,
                        assigned=True)
                    main_storage_phone.assigned = False
                    main_storage_phone.in_stock = True
                    main_storage_phone.sold = False
                    main_storage_phone.contract_no = '##'
                    main_storage_phone.sales_type = '##'
                    main_storage_phone.stock_out_date = main_storage_phone.entry_date
                    main_storage_phone.save()
                except MainStorage.DoesNotExist:
                    pass
            obj.delete()
    actions = [delete_selected]


@admin.register(CustomerData)
class CustomerDataAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "national_id",
                    "customer_contact", "second_contact", "customer_email",
                    "first_witness_name", "first_witness_contact",
                    "second_witness_name", "second_witness_contact",
                    "customer_location", "nearest_school",
                    "nearest_market_church_hospital", "created_at")
    search_fields = ('customer_name', 'customer_contact', 'national_id')
    

@admin.register(PhoneData)
class PhoneDataAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'agent_name', 'phone_name',
                    'imei_number', "contract_number", 'selling_price',
                    'cost_price', 'deposit', 'payment_period')
    search_fields = ('customer__customer_name', 'agent__user__username',
                     'phone_type', 'imei_number', 'contract_number')

    def customer_name(self, obj):
        return obj.customer.customer_name
    
    def agent_name(self, obj):
        return obj.agent.user.username

    def phone_name(self, obj):
        return obj.phone_type
    

@admin.register(UserAvatar)
class UserAvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')
    search_fields = ('user__username',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department')
    search_fields = ('user__username', 'role', 'department')
    fields = ('user', 'role', 'department')
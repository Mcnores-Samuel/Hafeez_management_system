from django.contrib import admin
from .models.customer_details import CustomerData
from .models.agent_profile import AgentProfile
from .models.customer_order import PhoneData
from .models.user_profile import UserProfile, UserAvatar
from .models.main_storage import MainStorage
from .models.reference import Phone_reference
from django.contrib.auth.admin import UserAdmin
from .models.user_profile import Employee
from .models.main_storage import Airtel_mifi_storage


admin.site.site_header = "HAFEEZ MANAGEMENT SYSTEM"
admin.site.site_title = "Hafeez"
admin.site.index_title = "Welcome to Hafeez Management System"


@admin.register(UserProfile)
class UserAdminModel(UserAdmin):
    list_display = (
        'email', 'username', 'first_name', 'last_name',
        'phone_number', 'location', 'is_staff', 'is_active', 'date_joined',
        'last_login'
    )


@admin.register(MainStorage)
class MainStorageData(admin.ModelAdmin):
    list_display = ('assigned_to', 'recieved', 'device_imei', 'category', 'name', 'phone_type',
                    'spec', 'screen_size', 'os', 'battery', 'camera', 'in_stock', 'pending', 'missing',
                    'sales_type', 'contract_no', 'assigned_from', 'updated_by', 'entry_date', 'stock_out_date',
                    'assigned', 'sold', 'paid', 'image', 'comment'
    )
    search_fields = ('device_imei', 'phone_type', 'entry_date', 'category', 'agent__username',
                     'contract_no', 'sales_type', 'stock_out_date', 'assigned', 'sold', 'paid')
    list_filter = ('in_stock', 'missing', 'category', 'updated_by', 'sales_type', 'assigned', 'sold', 'paid',
                   'entry_date', 'stock_out_date', 'assigned_from')
    
    list_per_page = 50

    actions = ['update_images', 'verify_stock_recieved',
               'unverify_stock_recieved', 'unassign_select', 'mark_as_sold',
               'missing']
    
    class Meta:
        ordering = ['-entry_date']
        js = ('/static/scripts/admin_autofill.js',)

    def assigned_to(self, obj):
        return obj.agent
    
    def missing(self, request, queryset):
        for obj in queryset:
            if obj:
                obj.missing = True
                obj.save()
    missing.short_description = "Mark as missing"


    def update_images(self, request, queryset):
        # Get the image from the first selected object
        image = queryset.first().image

        for phone in queryset:
            phone.image = image
            phone.save()
    update_images.short_description = "Update selected phones with the same image"
    
    def mark_as_sold(self, request, queryset):
        """Mark the phone as sold"""
        for obj in queryset:
            if obj:
                obj.in_stock = False
                obj.assigned = True
                obj.recieved = True
                obj.sold = True
                obj.save()
    mark_as_sold.short_description = "Mark as sold"

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

    def save_model(self, request, obj, form, change):
        """Override the save_model method to add the current user to the agent field"""
        data = MainStorage.objects.filter(name=obj.name,
                                          in_stock=True).first()

        # Auto fill the other fields with the related model
        if not change and data:
                obj.category = data.category
                obj.phone_type = data.phone_type
                obj.spec = data.spec
                obj.screen_size = data.screen_size
                obj.battery = data.battery
                obj.camera = data.camera
                obj.os = data.os
                obj.sales_type = data.sales_type
                obj.contract_no = data.contract_no
                if not obj.assigned_from:
                    obj.assigned_from = data.assigned_from
                obj.updated_by = request.user.username
                obj.recieved = True
                obj.assigned = True
                obj.save()
                return super().save_model(request, obj, form, change)
        obj.updated_by = request.user.username
        obj.save()
        return super().save_model(request, obj, form, change)


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


@admin.register(CustomerData)
class CustomerDataAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "approved", "pending", "rejected", "national_id",
                    "customer_contact", "second_contact", "customer_email",
                    "first_witness_name", "first_witness_contact",
                    "second_witness_name", "second_witness_contact",
                    "customer_location", "nearest_school",
                    "nearest_market_church_hospital", "created_at",
                    "workplace", "employer_or_coleague", "employer_or_coleague_contact",
                    "account_name")
    search_fields = ('customer_name', 'customer_contact', 'national_id')
    

@admin.register(PhoneData)
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
    

@admin.register(UserAvatar)
class UserAvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')
    search_fields = ('user__username',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department')
    search_fields = ('user__username', 'role', 'department')
    fields = ('user', 'role', 'department')


@admin.register(Airtel_mifi_storage)
class Airtel_mifi_storageAdmin(admin.ModelAdmin):
    """This model represent the entire stock available and sold in all posts"""
    list_display = ('assigned_to', 'recieved', 'device_imei', 'phone_number', 'secondary_phone_number', 'device',
                    'pending', 'active', 'inactive', 'in_stock',
                    'assigned', 'entry_date', 'stock_out_date',
                    'cash_recieved', 'paid', 'image', 'comment'
                    )
    
    search_fields = ('device_imei', 'device', 'entry_date',
                     'stock_out_date', 'agent__username')
    
    list_filter = ('in_stock', 'device', 'assigned', 'paid',
                     'entry_date', 'stock_out_date')

    def assigned_to(self, obj):
        """Return the agent to whom the phone is assigned"""
        return obj.agent
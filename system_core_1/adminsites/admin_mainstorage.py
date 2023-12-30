from django.contrib import admin
from ..models.main_storage import MainStorage
from ..customfilters.date_filters import YesterdayFilter
from ..customfilters.year_months_filter import YearMonthFilter
from ..models.special_orders import SpecialOrders
from ..models.reference import Price_reference
from django.utils import timezone


class MainStorageAdmin(admin.ModelAdmin):
    list_display = ('assigned_to', 'recieved', 'on_display', 'device_imei', 'category', 'name', 'phone_type',
                    'spec', 'screen_size', 'os', 'battery', 'camera', 'in_stock', 'pending', 'missing',
                    'sales_type', 'contract_no', 'assigned_from', 'updated_by', 'entry_date', 'stock_out_date',
                    'collected_on', 'assigned', 'sold', 'paid', 'image', 'comment', 'supplier'
    )
    search_fields = ('device_imei', 'name', 'phone_type', 'entry_date', 'category', 'agent__username',
                     'contract_no', 'sales_type', 'stock_out_date', 'assigned', 'sold', 'paid')
    list_filter = ('in_stock', 'on_display', 'missing', 'category', 'supplier', 'sales_type', 'assigned', 'sold', 'paid',
                   'entry_date', 'collected_on', 'stock_out_date', 'agent__username', YesterdayFilter, YearMonthFilter)
    
    list_per_page = 50

    actions = ['update_images', 'verify_stock_recieved',
               'unverify_stock_recieved', 'unassign_select', 'mark_as_sold',
               'missing', 'sum_special_orders']
    
    class Meta:
        ordering = ['-entry_date']

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

    def sum_special_orders(self, request, queryset):
        """Sum the special orders"""
        already_reset = False
        for obj in queryset:
            try:
                retailer = SpecialOrders.objects.get(presentative=obj.agent)
                price = Price_reference.objects.get(phone=obj.phone_type)
                if retailer.current_balance > 0 and not already_reset:
                    already_reset = True
                    retailer.current_balance = 0
                    retailer.current_orders = 0
                    retailer.updated_on = timezone.now()
                    retailer.save()
                retailer.current_balance += price.special_retailer_price
                retailer.current_orders += 1
                retailer.save()
            except SpecialOrders.DoesNotExist:
                pass
    sum_special_orders.short_description = "Sum special orders"


    def save_model(self, request, obj, form, change):
        """Override the save_model method to add the current user to the agent field"""
        data = MainStorage.objects.filter(name=obj.name,
                                          in_stock=True).first()
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
"""Admin classes for the refarbished phone models."""
from django.contrib import admin


class RefarbishedDevicesAdmin(admin.ModelAdmin):
  """RefarbishedDevices admin class for the admin panel."""
  list_display = ('held_by', 'device_name', 'model', 'total', 'previous_total', 
                  'cost', 'original_price', 'date_added', 'date_modified')
  search_fields = ('held_by__user__username', 'device_name')
  list_per_page = 20

  class Meta:
    ordering = ['-device_name']


class RefarbishedDevicesSalesAdmin(admin.ModelAdmin):
  """RefarbishedDevicesSales admin class for the admin panel."""
  list_display = ('device_name', 'model', 'total', 'cost', 'price_sold', 'profit', 
                  'date_sold', 'sold_by')
  search_fields = ('device_name', 'model', 'sold_by__user__username', 'date_sold')
  list_per_page = 20

  class Meta:
    ordering = ['-device_name']
"""Admin classes for the refarbished phone models."""
from django.contrib import admin


class RefarbishedDevicesAdmin(admin.ModelAdmin):
  """RefarbishedDevices admin class for the admin panel."""
  list_display = ('held_by', 'name', 'model', 'total', 'previous_total', 
                  'cost', 'date_added', 'date_modified')
  search_fields = ('held_by__user__username', 'name')
  list_per_page = 20

  class Meta:
    ordering = ['-name']


class RefarbishedDevicesSalesAdmin(admin.ModelAdmin):
  """RefarbishedDevicesSales admin class for the admin panel."""
  list_display = ('name', 'model', 'total', 'cost', 'price_sold', 'profit', 
                  'date_sold', 'sold_by')
  search_fields = ('name', 'model', 'sold_by__user__username', 'date_sold')
  list_per_page = 20

  class Meta:
    ordering = ['-name']
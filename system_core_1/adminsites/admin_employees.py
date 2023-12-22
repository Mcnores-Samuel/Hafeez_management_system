"""Admin site for employees site on the admin panel"""
from django.contrib import admin

class EmployeeAdmin(admin.ModelAdmin):
    """Employee admin class for the admin panel"""
    list_display = ('user', 'role', 'department')
    search_fields = ('user__username', 'role', 'department')
    fields = ('user', 'role', 'department')

    list_per_page = 20
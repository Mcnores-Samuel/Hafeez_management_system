"""Admin class for AgentProfile model."""
from django.contrib import admin


class AgentProfileAdmin(admin.ModelAdmin):
    """AgentProfile admin class for the admin panel."""
    list_display = ('user', 'is_agent', 'contact_number',
                    'location')
    search_fields = ('user__username', 'contact_number', 'location')

    list_per_page = 20

"""Admin site for user profile model."""
from django.contrib.auth.admin import UserAdmin
from ..forms.user_profile_update_form import UserProfileForm

class UserAdminModel(UserAdmin):
    """User admin model."""
    list_display = (
        'email', 'username', 'first_name', 'last_name',
        'phone_number', 'location', 'is_staff', 'is_active', 'date_joined',
        'last_login'
    )

    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    search_fields = ('email', 'username', 'first_name', 'last_name')

    ordering = ('email',)
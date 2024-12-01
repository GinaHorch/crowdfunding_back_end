from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Add organisation-specific fields to admin
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': (
                'role', 
                'organisation_name', 
                'organisation_contact', 
                'organisation_phone_number', 
                'organisation_ABN', 
                'is_charity', 
                'image_url'
            )
        }),
    )
    
    list_display = [
        'username', 
        'email', 
        'role', 
        'date_created', 
        'organisation_name', 
        'organisation_ABN', 
        'is_charity', 
        'is_active'
    ]
    list_filter = ['role', 'is_charity', 'is_active']  # Add filter for 'is_charity'
    search_fields = ['username', 'email', 'organisation_name', 'organisation_ABN']  # Add search fields for organisations

    def get_list_display(self, request):
        """Dynamically adjust list display based on role."""
        if request.user.is_superuser:
            return self.list_display
        return ['username', 'email', 'role', 'date_created']  # Limited fields for non-superusers
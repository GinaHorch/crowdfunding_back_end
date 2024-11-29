from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Display extra fields in admin
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'pledge_id', 'organisation_name', 'contact_person', 'phone_number', 'image_url', 'project')}),
    )
    list_display = ['username', 'email', 'role', 'date_created', 'is_active']
    list_filter = ['role', 'is_active']

admin.site.register(CustomUser, CustomUserAdmin)
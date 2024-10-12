from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Display extra fields in admin
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'pledge_id', 'organisation_name', 'contact_person', 'phone_number', 'image_url', 'project')}),
    )
    list_display = ['username', 'email', 'user_type', 'date_created']
    list_filter = ['user_type']

admin.site.register(CustomUser, CustomUserAdmin)
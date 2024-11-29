from django.contrib import admin
from .models import OrganisationProfile

# Register your models here.
@admin.register(OrganisationProfile)
class OrganisationProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'organisation_name', 'organisation_contact', 'organisation_ABN', 'is_charity']

from django.contrib import admin
from .models import Project, Pledge
from organisations.models import OrganisationProfile

# Register your models here
class PledgeInline(admin.TabularInline):
    model = Pledge
    extra = 1
class ProjectAdmin(admin.ModelAdmin):
    #Display extra fields in admin
    list_display = ('title', 'get_organisation_name', 'target_amount', 'current_amount', 'date_created')
    list_filter = ('organisation', 'is_open')
    search_fields = ('title', 'description')
    ordering = ('-date_created',)
    inlines = [PledgeInline]

    def get_organisation_name(self, obj):
        return obj.organisation.organisation_name
    get_organisation_name.short_description = 'Organisation Name'

admin.site.register(Project, ProjectAdmin)
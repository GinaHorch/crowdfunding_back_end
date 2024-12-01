from django.contrib import admin
from .models import Project, Pledge, Category
from users.models import CustomUser

# Register your models here
class PledgeInline(admin.TabularInline):
    model = Pledge
    extra = 1
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    #Display extra fields in admin
    list_display = ('title', 'get_organisation_name', 'target_amount', 'current_amount', 'is_open', 'date_created')
    list_filter = ('organisation', 'is_open')
    search_fields = ('title', 'description')
    ordering = ('-date_created',)
    inlines = [PledgeInline]

    def get_organisation_name(self, obj):
        return getattr(obj.organisation, 'organisation_name', 'No Organisation')
    #     return obj.organisation.organisation_name
    # get_organisation_name.admin_order_field = 'organisation__organisation_name'
    # get_organisation_name.short_description = 'Organisation Name'

@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    list_display = ('supporter', 'project', 'amount', 'anonymous', 'pledge_date')
    search_fields = ('supporter__username', 'project__title')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
from django.contrib import admin
from .models import Project, Pledge, Category
from users.models import CustomUser
from django.utils.html import format_html


# Register your models here
class PledgeInline(admin.TabularInline):
    model = Pledge
    extra = 1
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    #Display extra fields in admin
    list_display = ('title', 'get_organisation_name', 'target_amount', 'current_amount', 'is_open', 'date_created', 'image_preview')
    list_filter = ('organisation', 'is_open')
    search_fields = ('title', 'description')
    ordering = ('-date_created',)
    inlines = [PledgeInline]
    readonly_fields = ('image_preview',)

    # Include image field in the admin form
    fields = (
        'title',
        'description',
        'image',
        'image_preview',
        'target_amount',
        'current_amount',
        'location',
        'is_open',
        'date_created',
        'end_date',
        'category',
        'organisation',
    )


    def get_organisation_name(self, obj):
        return getattr(obj.organisation, 'organisation_name', 'No Organisation')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "-"

    image_preview.short_description = 'Image Preview'

@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    list_display = ('supporter', 'project', 'amount', 'anonymous', 'pledge_date')
    search_fields = ('supporter__username', 'project__title')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

def total_pledges(self, obj):
    return obj.pledges.aggregate(total=Sum('amount'))['total'] or 0
total_pledges.short_description = 'Total Pledged'

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'organisation_name', 'target_amount', 'total_pledges', 'remaining_amount']

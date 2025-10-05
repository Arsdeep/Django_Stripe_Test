# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Organization, OrgUser

# Register Organization model
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

# Customize UserAdmin for OrgUser
class OrgUserAdmin(UserAdmin):
    # Add 'organization' to the admin form
    fieldsets = UserAdmin.fieldsets + (
        ('Organization Info', {'fields': ('organization',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Organization Info', {'fields': ('organization',)}),
    )

    list_display = ('username', 'email', 'organization', 'is_staff', 'is_active')
    list_filter = ('organization', 'is_staff', 'is_superuser', 'is_active')

    search_fields = ('username', 'email', 'organization__name')
    ordering = ('username',)

# Register OrgUser
admin.site.register(OrgUser, OrgUserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    ordering = ['username']
    
    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات اضافی', {'fields': ('phone', 'bio')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('اطلاعات اضافی', {'fields': ('phone', 'bio')}),
    )

admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.Testimonial)
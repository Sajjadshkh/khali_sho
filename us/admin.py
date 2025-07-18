from django.contrib import admin
from . import models
from .models import Adviser, Certificate, Cafe, Owner, Podcast


class AdviserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'age', 'gender', 'is_unemployed', 'is_approved', 'is_featured')
    list_filter = ('gender', 'is_unemployed', 'is_approved', 'is_featured')
    search_fields = ('full_name', 'phone', 'email', 'bachelor_field', 'master_field', 'phd_field')
    list_editable = ('is_approved', 'is_featured')
    readonly_fields = ('latitude', 'longitude')

    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': ('full_name', 'phone', 'email', 'age', 'gender', 'location', 'latitude', 'longitude', 'address')
        }),
        ('تحصیلات', {
            'fields': (
                ('bachelor_field', 'bachelor_year'),
                ('master_field', 'master_year'),
                ('phd_field', 'phd_year'),
            )
        }),
        ('شغل و وضعیت کاری', {
            'fields': ('is_unemployed', 'current_position', 'current_organization', 'current_description')
        }),
        ('ترجیحات و تخصص‌ها', {
            'fields': ('work_preferences', 'specialties', 'consultation_methods')
        }),
        ('وضعیت', {
            'fields': ('accepted_terms', 'is_approved', 'is_featured')
        }),
    )


class CafeAdmin(admin.ModelAdmin):
    list_display = ('cafe_name', 'cafe_type', 'address', 'size', 'capacity', 'has_wifi', 'has_parking', 'has_live_music', 'has_outdoor', 'has_hookah', 'has_workspace', 'serves_breakfast', 'has_disabled_access', 'accepted_terms')
    search_fields = ('cafe_name', 'address')
    list_filter = ('cafe_type', 'has_wifi', 'has_parking', 'has_live_music', 'has_outdoor', 'has_hookah', 'has_workspace', 'serves_breakfast', 'has_disabled_access', 'accepted_terms')

class OwnerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'national_id', 'phone', 'email', 'cafe')
    search_fields = ('full_name', 'national_id', 'phone', 'email')
    list_filter = ('cafe',)

@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'accepted_rules', 'is_approved')
    search_fields = ('title', 'keywords')
    list_filter = ('category', 'created_at', 'is_approved')
    actions = ['approve_selected']

    @admin.action(description='تایید پادکست‌های انتخاب‌شده')
    def approve_selected(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} پادکست با موفقیت تأیید شد.')

admin.site.register(models.Aboutus)
admin.site.register(Adviser, AdviserAdmin)
admin.site.register(Certificate)
admin.site.register(Cafe, CafeAdmin)
admin.site.register(Owner, OwnerAdmin)
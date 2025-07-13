from django.contrib import admin
from . import models
from .models import adviser, Certificate, WORK_PREFERENCE_CHOICES, SPECIALTY_CHOICES, CONSULTATION_METHODS

# Helper dicts for value translation
WORK_PREF_DICT = dict(WORK_PREFERENCE_CHOICES)
SPECIALTY_DICT = dict(SPECIALTY_CHOICES)
CONSULTATION_DICT = dict(CONSULTATION_METHODS)

class AdviserAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'phone', 'email', 'age', 'gender', 'location', 'latitude', 'longitude',
        'get_work_preferences', 'get_specialties', 'get_consultation_methods'
    )
    fieldsets = (
        (None, {
            'fields': ('full_name', 'phone', 'email', 'age', 'gender', 'location', 'latitude', 'longitude')
        }),
        ('تحصیلات', {
            'fields': ('bachelor_field', 'bachelor_year', 'master_field', 'master_year', 'phd_field', 'phd_year')
        }),
        ('شغل', {
            'fields': ('is_unemployed', 'current_position', 'current_organization', 'current_description')
        }),
        ('سایر', {
            'fields': ('work_preferences', 'specialties', 'consultation_methods', 'accepted_terms')
        }),
    )
    readonly_fields = ('get_work_preferences', 'get_specialties', 'get_consultation_methods')

    def get_work_preferences(self, obj):
        return ', '.join([WORK_PREF_DICT.get(val, val) for val in obj.work_preferences])
    get_work_preferences.short_description = 'مایل به کار'

    def get_specialties(self, obj):
        return ', '.join([SPECIALTY_DICT.get(val, val) for val in obj.specialties])
    get_specialties.short_description = 'زمینه های تخصصی'

    def get_consultation_methods(self, obj):
        return ', '.join([CONSULTATION_DICT.get(val, val) for val in obj.consultation_methods])
    get_consultation_methods.short_description = 'روش های مشاوره'

admin.site.register(models.Aboutus)
admin.site.register(adviser, AdviserAdmin)
admin.site.register(Certificate)
from django.contrib import admin
from . import models
from .models import adviser, Certificate, Cafe, Owner, Podcast

class AdviserAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'phone', 'email', 'age', 'gender', 'location', 'latitude', 'longitude'
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
    list_display = ('title', 'category', 'created_at', 'accepted_rules')
    search_fields = ('title', 'keywords')
    list_filter = ('category', 'created_at')

admin.site.register(models.Aboutus)
admin.site.register(adviser, AdviserAdmin)
admin.site.register(Certificate)
admin.site.register(Cafe, CafeAdmin)
admin.site.register(Owner, OwnerAdmin)
from django.contrib import admin
from .models import Aboutus, OTP, Adviser, Certificate, Cafe, Owner, Podcast, Plan, Cart, CartItem, Order, OrderItem


class AdviserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'age', 'gender', 'is_unemployed', 'is_approved', 'is_featured')
    list_filter = ('gender', 'is_unemployed', 'is_approved', 'is_featured')
    search_fields = ('full_name', 'phone', 'email', 'bachelor_field', 'master_field', 'phd_field')
    list_editable = ('is_approved', 'is_featured')
    readonly_fields = ('latitude', 'longitude')

    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': ('full_name', 'phone', 'image', 'email', 'age', 'gender', 'location', 'latitude', 'longitude', 'address')
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
    list_display = ('cafe_name', 'cafe_type', 'address', 'size', 'capacity', 'image', 'has_wifi', 'has_parking', 'has_live_music', 'has_outdoor', 'has_hookah', 'has_workspace', 'serves_breakfast', 'has_disabled_access', 'accepted_terms', 'is_featured')
    search_fields = ('cafe_name', 'address')
    list_filter = ('cafe_type', 'has_wifi', 'has_parking', 'has_live_music', 'has_outdoor', 'has_hookah', 'has_workspace', 'serves_breakfast', 'has_disabled_access', 'accepted_terms', 'is_featured')
    list_editable = ('is_featured',)
    readonly_fields = ()
    fieldsets = (
        (None, {
            'fields': ('cafe_name', 'cafe_type', 'address', 'size', 'capacity', 'menu_file', 'image', 'description', 'latitude', 'longitude',
                       'has_wifi', 'has_parking', 'has_live_music', 'has_outdoor', 'has_hookah', 'has_workspace', 'serves_breakfast', 'has_disabled_access', 'accepted_terms', 'is_featured')
        }),
    )

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

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'duration', 'extra_time', 'price', 'is_active', 'created_at']
    list_filter = ['plan_type', 'is_active', 'created_at']
    search_fields = ['name']
    ordering = ['price']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'created_at', 'updated_at', 'get_total_price']
    search_fields = ['session_key']
    ordering = ['-created_at']
    
    def get_total_price(self, obj):
        return f"{obj.get_total_price():,} تومان"
    get_total_price.short_description = 'مجموع کل'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'plan', 'quantity', 'get_total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['plan__name']
    
    def get_total_price(self, obj):
        return f"{obj.get_total_price():,} تومان"
    get_total_price.short_description = 'قیمت کل'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'phone', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'user']
    search_fields = ['order_number', 'phone', 'user__username']
    ordering = ['-created_at']
    readonly_fields = ['order_number', 'created_at', 'updated_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'plan', 'quantity', 'price', 'total_price']
    list_filter = ['plan__plan_type']
    search_fields = ['order__order_number', 'plan__name']

admin.site.register(Aboutus)
admin.site.register(Adviser, AdviserAdmin)
admin.site.register(Certificate)
admin.site.register(Cafe, CafeAdmin)
admin.site.register(Owner, OwnerAdmin)
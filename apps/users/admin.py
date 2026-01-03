"""
User admin configuration.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Currency, Language, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin interface for global site settings."""
    list_display = ['site_name', 'currency', 'language', 'updated_at']
    readonly_fields = ('updated_at',)
    
    fieldsets = (
        ('General Settings', {
            'fields': ('site_name',)
        }),
        ('Localization', {
            'fields': ('currency', 'language'),
            'description': 'These settings will apply to all users on the platform'
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one settings instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of settings
        return False


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    """Admin interface for Currency model."""
    list_display = ['code', 'name', 'symbol', 'exchange_rate', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['code', 'name']
    ordering = ['name']
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Currency Information', {
            'fields': ('code', 'name', 'symbol')
        }),
        ('Exchange Rate', {
            'fields': ('exchange_rate',),
            'description': 'Exchange rate relative to USD (1 USD = X in this currency)'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    """Admin interface for Language model."""
    list_display = ['code', 'name', 'native_name', 'is_rtl', 'is_active', 'updated_at']
    list_filter = ['is_active', 'is_rtl', 'created_at']
    search_fields = ['code', 'name', 'native_name']
    ordering = ['name']
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Language Information', {
            'fields': ('code', 'name', 'native_name')
        }),
        ('Settings', {
            'fields': ('is_rtl', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    view_on_site = True
    list_display = [
        'email', 'username', 'first_name', 'last_name', 
        'balance', 'is_verified', 'created_at'
    ]
    list_filter = ['is_verified', 'created_at', 'is_staff']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']
    readonly_fields = ('last_login', 'created_at', 'updated_at')
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'profile_image')}),
        ('Investment Info', {'fields': ('balance', 'total_invested', 'total_earnings')}),
        ('Contact Info', {'fields': ('phone_number', 'country')}),
        ('Verification', {'fields': ('is_verified', 'verification_code')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    def get_view_on_site_url(self, obj=None):
        if obj is None:
            return None
        try:
            return obj.get_absolute_url()
        except Exception:
            return None

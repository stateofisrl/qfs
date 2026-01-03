"""
Investment admin configuration.
"""

from django.contrib import admin
from .models import InvestmentPlan, UserInvestment


@admin.register(InvestmentPlan)
class InvestmentPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'roi_percentage', 'duration_days', 'minimum_investment', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['roi_percentage']


@admin.register(UserInvestment)
class UserInvestmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'amount', 'status', 'start_date', 'end_date']
    list_filter = ['status', 'plan', 'created_at']
    search_fields = ['user__email', 'plan__name']
    ordering = ['-created_at']
    
    def get_readonly_fields(self, request, obj=None):
        """Make fields readonly only when editing existing investment."""
        if obj:  # Editing existing investment
            return ['user', 'plan', 'amount', 'start_date', 'expected_return', 'created_at', 'updated_at']
        return []  # Adding new investment - allow editing all fields
    
    def get_fieldsets(self, request, obj=None):
        """Return different fieldsets for add vs change forms."""
        if obj:  # Editing existing investment
            return (
                ('Investment Info', {
                    'fields': ('user', 'plan', 'amount')
                }),
                ('Dates', {
                    'fields': ('start_date', 'end_date')
                }),
                ('Returns', {
                    'fields': ('expected_return', 'earned')
                }),
                ('Status', {
                    'fields': ('status',)
                }),
                ('System', {
                    'fields': ('created_at', 'updated_at'),
                    'classes': ('collapse',)
                }),
            )
        else:  # Adding new investment
            return (
                ('Investment Info', {
                    'fields': ('user', 'plan', 'amount')
                }),
                ('Dates', {
                    'fields': ('end_date',)
                }),
                ('Returns', {
                    'fields': ('earned',)
                }),
                ('Status', {
                    'fields': ('status',)
                }),
            )

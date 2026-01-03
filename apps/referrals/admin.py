"""
Admin configuration for Referral app.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import ReferralSettings, Referral, ReferralCommission
from .models import CommissionTransaction


@admin.register(ReferralSettings)
class ReferralSettingsAdmin(admin.ModelAdmin):
    """Admin interface for referral settings."""
    
    list_display = [
        'commission_percentage',
        'is_active',
        'minimum_deposit_for_commission',
        'max_commission_amount',
        'welcome_bonus_enabled',
        'welcome_bonus_amount',
        'withdrawal_fee_percentage',
        'updated_at'
    ]
    
    fieldsets = (
        ('Commission Settings', {
            'fields': ('commission_percentage', 'minimum_deposit_for_commission', 'max_commission_amount')
        }),
        ('Welcome Bonus', {
            'fields': ('welcome_bonus_enabled', 'welcome_bonus_amount', 'welcome_bonus_message')
        }),
        ('Withdrawal Fee for Bonus Users', {
            'fields': ('withdrawal_fee_percentage',),
            'description': 'Apply a withdrawal fee to users who received welcome bonus from referrals'
        }),
        ('System Settings', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one settings instance
        return not ReferralSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of settings
        return False


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    """Admin interface for referrals."""
    
    list_display = [
        'id',
        'referrer_info',
        'referred_info',
        'total_commissions',
        'created_at'
    ]
    list_filter = ['created_at']
    search_fields = [
        'referrer__username',
        'referrer__email',
        'referred__username',
        'referred__email'
    ]
    raw_id_fields = ['referrer', 'referred']
    
    def get_readonly_fields(self, request, obj=None):
        """Make fields readonly only when editing existing referral."""
        if obj:  # Editing existing referral
            return ['created_at']
        return []  # Adding new referral - allow editing all fields
    
    def referrer_info(self, obj):
        return format_html(
            '<strong>{}</strong><br>{}',
            obj.referrer.username,
            obj.referrer.email
        )
    referrer_info.short_description = 'Referrer'
    
    def referred_info(self, obj):
        return format_html(
            '<strong>{}</strong><br>{}',
            obj.referred.username,
            obj.referred.email
        )
    referred_info.short_description = 'Referred User'
    
    def total_commissions(self, obj):
        total = sum(c.amount for c in obj.commissions.filter(status='paid'))
        return f"${total:.2f}"
    total_commissions.short_description = 'Total Paid Commissions'


@admin.register(ReferralCommission)
class ReferralCommissionAdmin(admin.ModelAdmin):
    """Admin interface for referral commissions."""
    
    list_display = [
        'id',
        'referrer_name',
        'referred_name',
        'amount_display',
        'deposit_amount',
        'status_badge',
        'created_at',
        'paid_at'
    ]
    list_filter = ['status', 'created_at', 'paid_at']
    search_fields = [
        'referral__referrer__username',
        'referral__referrer__email',
        'referral__referred__username',
        'referral__referred__email'
    ]
    actions = ['mark_as_paid', 'mark_as_cancelled']
    
    def get_readonly_fields(self, request, obj=None):
        """Make fields readonly only when editing existing commission."""
        if obj:  # Editing existing commission
            return ['referral', 'deposit', 'amount', 'created_at', 'paid_at']
        return []  # Adding new commission - allow editing all fields
    
    def get_fieldsets(self, request, obj=None):
        """Return different fieldsets for add vs change forms."""
        if obj:  # Editing existing commission
            return (
                ('Commission Info', {
                    'fields': ('referral', 'deposit', 'amount')
                }),
                ('Status', {
                    'fields': ('status',)
                }),
                ('Dates', {
                    'fields': ('created_at', 'paid_at'),
                    'classes': ('collapse',)
                }),
            )
        else:  # Adding new commission
            return (
                ('Commission Info', {
                    'fields': ('referral', 'deposit', 'amount')
                }),
                ('Status', {
                    'fields': ('status',)
                }),
            )
    
    def referrer_name(self, obj):
        return obj.referral.referrer.username
    referrer_name.short_description = 'Referrer'
    
    def referred_name(self, obj):
        return obj.referral.referred.username
    referred_name.short_description = 'Referred User'
    
    def amount_display(self, obj):
        return f"${obj.amount:.2f}"
    amount_display.short_description = 'Commission Amount'
    
    def deposit_amount(self, obj):
        return f"${obj.deposit.amount:.2f}"
    deposit_amount.short_description = 'Deposit Amount'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'paid': '#28a745',
            'cancelled': '#dc3545'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def mark_as_paid(self, request, queryset):
        """Action to mark selected commissions as paid."""
        count = 0
        for commission in queryset.filter(status='pending'):
            commission.mark_as_paid()
            count += 1
        self.message_user(request, f'{count} commission(s) marked as paid and added to user balances.')
    mark_as_paid.short_description = 'Mark selected as paid'
    
    def mark_as_cancelled(self, request, queryset):
        """Action to mark selected commissions as cancelled."""
        count = queryset.filter(status='pending').update(status='cancelled')
        self.message_user(request, f'{count} commission(s) marked as cancelled.')
    mark_as_cancelled.short_description = 'Mark selected as cancelled'

@admin.register(CommissionTransaction)
class CommissionTransactionAdmin(admin.ModelAdmin):
    """Admin interface for commission transactions."""
    
    list_display = ['user', 'amount_display', 'transaction_type', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['commission', 'user', 'amount', 'transaction_type', 'created_at']
    
    def amount_display(self, obj):
        return f"${obj.amount:.2f}"
    amount_display.short_description = 'Amount'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Allow superusers to delete transactions (needed for user deletion cascade)
        return request.user.is_superuser

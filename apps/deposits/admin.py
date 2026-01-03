"""
Deposits admin configuration.
"""

from django.contrib import admin
from django.utils import timezone
from decimal import Decimal
from .models import Deposit, CryptoWallet


@admin.register(CryptoWallet)
class CryptoWalletAdmin(admin.ModelAdmin):
    list_display = ['cryptocurrency', 'wallet_address', 'is_active', 'created_at']
    list_filter = ['is_active', 'cryptocurrency']
    search_fields = ['cryptocurrency', 'wallet_address']
    ordering = ['cryptocurrency']


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ['user', 'cryptocurrency', 'currency_amount_display', 'amount', 'status', 'created_at']
    list_filter = ['status', 'cryptocurrency', 'created_at']
    search_fields = ['user__email', 'cryptocurrency']
    # Allow entering proof content when creating deposits via admin
    readonly_fields = ['currency_amount_display']
    actions = ['approve_deposit', 'reject_deposit']
    ordering = ['-created_at']
    
    fieldsets = (
        ('User & Deposit Info', {
            'fields': ('user', 'cryptocurrency', 'currency_amount_display', 'amount', 'created_at')
        }),
        ('Proof Details', {
            'fields': ('proof_type', 'proof_content', 'proof_image')
        }),
        ('Status & Admin Actions', {
            'fields': ('status', 'admin_notes', 'approved_by', 'approved_at')
        }),
    )
    
    def currency_amount_display(self, obj):
        """Display currency amount with symbol (convert from USD to current platform currency)."""
        if obj.currency_amount:
            from apps.users.models import SiteSettings
            try:
                settings = SiteSettings.get_settings()
                symbol = settings.currency.symbol if settings.currency else '$'
                exchange_rate = settings.currency.exchange_rate if settings.currency else Decimal('1')
                # Convert USD back to platform currency for display
                platform_amount = obj.currency_amount * exchange_rate
                return f"{symbol}{platform_amount}"
            except:
                return f"${obj.currency_amount}"
        return "N/A"
    currency_amount_display.short_description = "Amount in Platform Currency"
    
    def approve_deposit(self, request, queryset):
        """Admin action to approve deposits. Do NOT set approved_at here; signal will stamp it after crediting."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        approved_count = 0
        for deposit in queryset.filter(status='pending'):
            deposit.status = 'approved'
            # Do NOT set approved_at here; let the signal credit balance and stamp it
            deposit.approved_by = request.user
            deposit.save()
            
            approved_count += 1
        
        self.message_user(request, f'{approved_count} deposit(s) approved successfully.')
    
    approve_deposit.short_description = 'Approve selected deposits'
    
    def reject_deposit(self, request, queryset):
        """Admin action to reject deposits."""
        rejected_count = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'{rejected_count} deposit(s) rejected.')
    
    reject_deposit.short_description = 'Reject selected deposits'

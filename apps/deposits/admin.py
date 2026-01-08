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
    list_display = ['user', 'get_crypto_symbol', 'currency_amount_display', 'amount', 'proof_type', 'get_proof_display', 'status', 'created_at']
    list_filter = ['status', 'cryptocurrency', 'proof_type', 'created_at']
    search_fields = ['user__email', 'cryptocurrency']
    # Allow entering proof content when creating deposits via admin
    readonly_fields = ['currency_amount_display', 'proof_image_preview']
    actions = ['approve_deposit', 'reject_deposit']
    ordering = ['-created_at']
    
    fieldsets = (
        ('User & Deposit Info', {
            'fields': ('user', 'cryptocurrency', 'currency_amount_display', 'amount', 'created_at')
        }),
        ('Proof Details', {
            'fields': ('proof_type', 'proof_content', 'proof_image', 'proof_image_preview')
        }),
        ('Status & Admin Actions', {
            'fields': ('status', 'admin_notes', 'approved_by', 'approved_at')
        }),
    )
    
    def get_crypto_symbol(self, obj):
        """Display cryptocurrency symbol only."""
        crypto_symbols = {
            'Bitcoin': 'BTC',
            'Ethereum': 'ETH',
            'Tether': 'USDT',
            'BNB': 'BNB',
            'Solana': 'SOL',
            'USDC': 'USDC',
            'XRP': 'XRP',
            'Cardano': 'ADA',
            'Dogecoin': 'DOGE',
            'TRON': 'TRX',
            'Toncoin': 'TON',
            'Chainlink': 'LINK',
            'Avalanche': 'AVAX',
            'Shiba Inu': 'SHIB',
            'Bitcoin Cash': 'BCH',
            'Polkadot': 'DOT',
            'Dai': 'DAI',
            'Litecoin': 'LTC',
            'NEAR Protocol': 'NEAR',
            'Uniswap': 'UNI',
            'LEO Token': 'LEO',
            'Wrapped Bitcoin': 'WBTC',
            'Aptos': 'APT',
            'Internet Computer': 'ICP',
            'Polygon': 'MATIC',
            'Ethereum Classic': 'ETC',
            'Stellar': 'XLM',
            'Render': 'RNDR',
            'Monero': 'XMR',
            'OKB': 'OKB',
            'Filecoin': 'FIL'
        }
        return crypto_symbols.get(obj.cryptocurrency, obj.cryptocurrency)
    get_crypto_symbol.short_description = 'Crypto'
    
    def get_proof_display(self, obj):
        """Display proof information in list view."""
        if obj.proof_type == 'screenshot' and obj.proof_image:
            return '📷 Screenshot attached'
        elif obj.proof_content:
            return obj.proof_content[:50] + '...' if len(obj.proof_content) > 50 else obj.proof_content
        return 'No proof'
    get_proof_display.short_description = 'Proof'
    
    def proof_image_preview(self, obj):
        """Display proof image preview in detail view."""
        if obj.proof_image:
            from django.utils.html import format_html
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-width: 300px; max-height: 300px;" /></a>',
                obj.proof_image.url,
                obj.proof_image.url
            )
        return 'No image'
    proof_image_preview.short_description = 'Proof Image Preview'
    
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

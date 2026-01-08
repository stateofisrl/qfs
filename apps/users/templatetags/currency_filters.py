"""
Custom template filters for currency conversion.
"""

from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()


@register.filter
def convert_currency(amount, exchange_rate=None):
    """
    Convert USD amount to the selected currency using exchange rate.
    Usage: {{ amount|convert_currency:site_currency.exchange_rate }}
    """
    if amount is None:
        return 0
    
    try:
        amount = Decimal(str(amount))
        if exchange_rate:
            exchange_rate = Decimal(str(exchange_rate))
            return amount * exchange_rate
        return amount
    except (ValueError, TypeError, InvalidOperation):
        return amount


@register.filter
def format_currency(amount, currency_info=None):
    """
    Format amount with currency symbol and proper conversion.
    Usage: {{ amount|format_currency:site_currency }}
    """
    if amount is None:
        return f"0.00"
    
    try:
        amount = Decimal(str(amount))
        
        # If currency_info is provided (currency object), apply exchange rate
        if currency_info and hasattr(currency_info, 'exchange_rate'):
            exchange_rate = Decimal(str(currency_info.exchange_rate))
            converted_amount = amount * exchange_rate
            symbol = currency_info.symbol
            return f"{symbol}{converted_amount:,.2f}"
        
        # Default to USD
        return f"${amount:,.2f}"
    except (ValueError, TypeError, AttributeError):
        return f"${amount}"


@register.simple_tag(takes_context=True)
def currency_display(context, amount):
    """
    Display amount with proper currency conversion.
    Usage: {% currency_display amount %}
    """
    site_currency = context.get('site_currency')
    
    if amount is None:
        amount = 0
    
    try:
        amount = Decimal(str(amount))
        
        if site_currency:
            exchange_rate = Decimal(str(site_currency.exchange_rate))
            converted_amount = amount * exchange_rate
            symbol = site_currency.symbol
            return f"{symbol}{converted_amount:,.2f}"
        
        return f"${amount:,.2f}"
    except (ValueError, TypeError, AttributeError):
        return f"${amount}"

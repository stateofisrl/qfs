"""
Celery tasks for users app.
"""

from celery import shared_task
from django.core.management import call_command
from django.core.cache import cache


@shared_task
def update_crypto_and_exchange_rates():
    """
    Periodic task to update cryptocurrency prices and exchange rates.
    Runs every hour via Celery Beat.
    """
    try:
        # Step 1: Update exchange rates
        print("📊 [Celery Task] Updating exchange rates...")
        call_command('update_exchange_rates')
        
        # Step 2: Clear crypto price cache
        print("🔄 [Celery Task] Clearing crypto price cache...")
        cache.delete('crypto_prices_usd')
        
        # Step 3: Fetch fresh crypto prices
        print("💰 [Celery Task] Fetching fresh crypto prices...")
        from apps.deposits.crypto_prices import get_real_crypto_prices
        prices = get_real_crypto_prices()
        
        print(f"✅ [Celery Task] Successfully updated prices. {len(prices)} cryptocurrencies updated.")
        return {
            'status': 'success',
            'crypto_count': len(prices),
            'message': 'Prices updated successfully'
        }
        
    except Exception as e:
        error_msg = f"❌ [Celery Task] Error updating prices: {str(e)}"
        print(error_msg)
        return {
            'status': 'error',
            'message': str(e)
        }

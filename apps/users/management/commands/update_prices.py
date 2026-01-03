"""
Update both cryptocurrency prices and exchange rates.
Run with: python manage.py update_prices
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Update cryptocurrency prices and exchange rates'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🔄 Starting price updates...\n'))
        
        # Update exchange rates
        self.stdout.write(self.style.SUCCESS('Step 1: Updating exchange rates'))
        call_command('update_exchange_rates')
        
        # Clear crypto price cache to force refresh
        self.stdout.write(self.style.SUCCESS('\nStep 2: Clearing crypto price cache'))
        from django.core.cache import cache
        cache.delete('crypto_prices_usd')
        self.stdout.write(self.style.SUCCESS('  ✓ Crypto price cache cleared\n'))
        
        # Fetch new crypto prices
        self.stdout.write(self.style.SUCCESS('Step 3: Fetching fresh crypto prices'))
        from apps.deposits.crypto_prices import get_real_crypto_prices
        prices = get_real_crypto_prices()
        
        for crypto, price in prices.items():
            self.stdout.write(f'  💰 {crypto}: ${price:,.2f}')
        
        self.stdout.write(self.style.SUCCESS('\n✨ All prices updated successfully!\n'))

"""
Update currency exchange rates from real-time API.
Run with: python manage.py update_exchange_rates
"""

import requests
from decimal import Decimal
from django.core.management.base import BaseCommand
from apps.users.models import Currency


class Command(BaseCommand):
    help = 'Update currency exchange rates from exchangerate-api.com'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n💱 Updating exchange rates from API...\n'))
        
        try:
            # Free API from exchangerate-api.com (no API key needed for basic usage)
            url = 'https://api.exchangerate-api.com/v4/latest/USD'
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f'❌ API Error: {response.status_code}'))
                return
            
            data = response.json()
            rates = data.get('rates', {})
            
            if not rates:
                self.stdout.write(self.style.ERROR('❌ No rates found in API response'))
                return
            
            updated_count = 0
            
            # Get all currencies from database
            currencies = Currency.objects.all()
            
            for currency in currencies:
                code = currency.code
                
                # USD is always 1.0
                if code == 'USD':
                    if currency.exchange_rate != Decimal('1.00'):
                        currency.exchange_rate = Decimal('1.00')
                        currency.save()
                        self.stdout.write(f'  ✓ {code}: 1.00 (base currency)')
                        updated_count += 1
                    continue
                
                # Get rate from API
                if code in rates:
                    new_rate = Decimal(str(rates[code]))
                    old_rate = currency.exchange_rate
                    
                    if old_rate != new_rate:
                        currency.exchange_rate = new_rate
                        currency.save()
                        
                        change_percent = ((new_rate - old_rate) / old_rate * 100) if old_rate else 0
                        symbol = '📈' if change_percent > 0 else '📉' if change_percent < 0 else '➡️'
                        
                        self.stdout.write(f'  {symbol} {code}: {old_rate} → {new_rate} ({change_percent:+.2f}%)')
                        updated_count += 1
                    else:
                        self.stdout.write(f'  ➡️  {code}: {new_rate} (no change)')
                else:
                    self.stdout.write(self.style.WARNING(f'  ⚠️  {code}: Not found in API'))
            
            self.stdout.write(self.style.SUCCESS(f'\n✨ Updated {updated_count} exchange rate(s)\n'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error updating exchange rates: {str(e)}'))
            import traceback
            traceback.print_exc()

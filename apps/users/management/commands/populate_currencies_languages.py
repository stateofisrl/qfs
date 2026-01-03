"""
Management command to populate initial currencies and languages.
"""

from django.core.management.base import BaseCommand
from apps.users.models import Currency, Language


class Command(BaseCommand):
    help = 'Populate initial currencies and languages in the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating currencies...')
        
        # Create currencies
        currencies_data = [
            {'code': 'USD', 'name': 'US Dollar', 'symbol': '$', 'exchange_rate': 1.0000},
            {'code': 'EUR', 'name': 'Euro', 'symbol': '€', 'exchange_rate': 0.9200},
            {'code': 'GBP', 'name': 'British Pound', 'symbol': '£', 'exchange_rate': 0.7900},
            {'code': 'JPY', 'name': 'Japanese Yen', 'symbol': '¥', 'exchange_rate': 149.5000},
            {'code': 'CAD', 'name': 'Canadian Dollar', 'symbol': 'C$', 'exchange_rate': 1.3500},
            {'code': 'AUD', 'name': 'Australian Dollar', 'symbol': 'A$', 'exchange_rate': 1.5200},
            {'code': 'CHF', 'name': 'Swiss Franc', 'symbol': 'CHF', 'exchange_rate': 0.8800},
            {'code': 'CNY', 'name': 'Chinese Yuan', 'symbol': '¥', 'exchange_rate': 7.2400},
            {'code': 'INR', 'name': 'Indian Rupee', 'symbol': '₹', 'exchange_rate': 83.2000},
            {'code': 'NGN', 'name': 'Nigerian Naira', 'symbol': '₦', 'exchange_rate': 1475.0000},
            {'code': 'ZAR', 'name': 'South African Rand', 'symbol': 'R', 'exchange_rate': 18.5000},
            {'code': 'BRL', 'name': 'Brazilian Real', 'symbol': 'R$', 'exchange_rate': 4.9500},
            {'code': 'MXN', 'name': 'Mexican Peso', 'symbol': 'Mex$', 'exchange_rate': 17.1000},
            {'code': 'RUB', 'name': 'Russian Ruble', 'symbol': '₽', 'exchange_rate': 92.5000},
            {'code': 'AED', 'name': 'UAE Dirham', 'symbol': 'د.إ', 'exchange_rate': 3.6700},
        ]
        
        created_currencies = 0
        for currency_data in currencies_data:
            currency, created = Currency.objects.get_or_create(
                code=currency_data['code'],
                defaults=currency_data
            )
            if created:
                created_currencies += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created currency: {currency.code} - {currency.name}'))
            else:
                self.stdout.write(f'  Currency already exists: {currency.code}')
        
        self.stdout.write(self.style.SUCCESS(f'\nTotal currencies created: {created_currencies}/{len(currencies_data)}'))
        
        # Create languages
        self.stdout.write('\n\nPopulating languages...')
        
        languages_data = [
            {'code': 'en', 'name': 'English', 'native_name': 'English', 'is_rtl': False},
            {'code': 'es', 'name': 'Spanish', 'native_name': 'Español', 'is_rtl': False},
            {'code': 'fr', 'name': 'French', 'native_name': 'Français', 'is_rtl': False},
            {'code': 'de', 'name': 'German', 'native_name': 'Deutsch', 'is_rtl': False},
            {'code': 'it', 'name': 'Italian', 'native_name': 'Italiano', 'is_rtl': False},
            {'code': 'pt', 'name': 'Portuguese', 'native_name': 'Português', 'is_rtl': False},
            {'code': 'ru', 'name': 'Russian', 'native_name': 'Русский', 'is_rtl': False},
            {'code': 'zh', 'name': 'Chinese', 'native_name': '中文', 'is_rtl': False},
            {'code': 'ja', 'name': 'Japanese', 'native_name': '日本語', 'is_rtl': False},
            {'code': 'ar', 'name': 'Arabic', 'native_name': 'العربية', 'is_rtl': True},
            {'code': 'hi', 'name': 'Hindi', 'native_name': 'हिन्दी', 'is_rtl': False},
            {'code': 'tr', 'name': 'Turkish', 'native_name': 'Türkçe', 'is_rtl': False},
            {'code': 'nl', 'name': 'Dutch', 'native_name': 'Nederlands', 'is_rtl': False},
            {'code': 'pl', 'name': 'Polish', 'native_name': 'Polski', 'is_rtl': False},
            {'code': 'ko', 'name': 'Korean', 'native_name': '한국어', 'is_rtl': False},
        ]
        
        created_languages = 0
        for language_data in languages_data:
            language, created = Language.objects.get_or_create(
                code=language_data['code'],
                defaults=language_data
            )
            if created:
                created_languages += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created language: {language.code} - {language.name} ({language.native_name})'))
            else:
                self.stdout.write(f'  Language already exists: {language.code}')
        
        self.stdout.write(self.style.SUCCESS(f'\nTotal languages created: {created_languages}/{len(languages_data)}'))
        self.stdout.write(self.style.SUCCESS('\n✅ Done! You can now manage currencies and languages from the admin panel.'))

from django.core.management.base import BaseCommand
from apps.users.models import Currency, Language


class Command(BaseCommand):
    help = 'Populate currencies and languages in database'

    def handle(self, *args, **options):
        # Create Currencies
        currencies_data = [
            ('USD', 'US Dollar', '$', 1.00),
            ('EUR', 'Euro', '€', 0.92),
            ('GBP', 'British Pound', '£', 0.79),
            ('AUD', 'Australian Dollar', 'A$', 1.52),
            ('CAD', 'Canadian Dollar', 'C$', 1.36),
            ('CHF', 'Swiss Franc', 'CHF', 0.88),
            ('JPY', 'Japanese Yen', '¥', 149.50),
            ('CNY', 'Chinese Yuan', '¥', 7.24),
            ('INR', 'Indian Rupee', '₹', 83.12),
            ('RUB', 'Russian Ruble', '₽', 92.50),
            ('BRL', 'Brazilian Real', 'R$', 4.97),
            ('MXN', 'Mexican Peso', 'Mex$', 17.08),
            ('ZAR', 'South African Rand', 'R', 18.65),
            ('NGN', 'Nigerian Naira', '₦', 1505.00),
            ('AED', 'UAE Dirham', 'د.إ', 3.67),
        ]
        
        created_currencies = 0
        for code, name, symbol, rate in currencies_data:
            currency, created = Currency.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'symbol': symbol,
                    'exchange_rate': rate,
                    'is_active': True
                }
            )
            if created:
                created_currencies += 1
                self.stdout.write(f'Created: {code} - {name}')
        
        # Create Languages
        languages_data = [
            ('en', 'English', 'English', False),
            ('es', 'Spanish', 'Español', False),
            ('fr', 'French', 'Français', False),
            ('de', 'German', 'Deutsch', False),
            ('it', 'Italian', 'Italiano', False),
            ('pt', 'Portuguese', 'Português', False),
            ('ru', 'Russian', 'Русский', False),
            ('ar', 'Arabic', 'العربية', True),
            ('zh', 'Chinese', '中文', False),
            ('ja', 'Japanese', '日本語', False),
            ('ko', 'Korean', '한국어', False),
            ('hi', 'Hindi', 'हिन्दी', False),
            ('tr', 'Turkish', 'Türkçe', False),
            ('nl', 'Dutch', 'Nederlands', False),
            ('pl', 'Polish', 'Polski', False),
        ]
        
        created_languages = 0
        for code, name, native_name, is_rtl in languages_data:
            language, created = Language.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'native_name': native_name,
                    'is_rtl': is_rtl,
                    'is_active': True
                }
            )
            if created:
                created_languages += 1
                self.stdout.write(f'Created: {code} - {name}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Done! Created {created_currencies} currencies and {created_languages} languages'
            )
        )

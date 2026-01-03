"""
Management command to initialize site settings.
"""

from django.core.management.base import BaseCommand
from apps.users.models import Currency, Language, SiteSettings


class Command(BaseCommand):
    help = 'Initialize site settings with default currency and language'

    def handle(self, *args, **kwargs):
        self.stdout.write('Setting up site settings...')
        
        # Check if settings already exist
        if SiteSettings.objects.exists():
            settings = SiteSettings.objects.first()
            self.stdout.write(self.style.WARNING(f'Site settings already exist:'))
            self.stdout.write(f'  Currency: {settings.currency}')
            self.stdout.write(f'  Language: {settings.language}')
            return
        
        # Get USD and English as defaults
        usd = Currency.objects.filter(code='USD').first()
        english = Language.objects.filter(code='en').first()
        
        if not usd:
            self.stdout.write(self.style.ERROR('USD currency not found. Please run: python manage.py populate_currencies_languages'))
            return
        
        if not english:
            self.stdout.write(self.style.ERROR('English language not found. Please run: python manage.py populate_currencies_languages'))
            return
        
        # Create site settings
        settings = SiteSettings.objects.create(
            site_name='Tesla Investment Platform',
            currency=usd,
            language=english
        )
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Site settings created successfully!'))
        self.stdout.write(f'  Site Name: {settings.site_name}')
        self.stdout.write(f'  Default Currency: {settings.currency}')
        self.stdout.write(f'  Default Language: {settings.language}')
        self.stdout.write(f'\nYou can change these settings in the admin panel:')
        self.stdout.write(f'  Admin → Users → Site Settings')

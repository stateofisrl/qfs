"""
User models for Investment Platform.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class Currency(models.Model):
    """Currency model for multi-currency support."""
    
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('JPY', 'Japanese Yen'),
        ('CAD', 'Canadian Dollar'),
        ('AUD', 'Australian Dollar'),
        ('CHF', 'Swiss Franc'),
        ('CNY', 'Chinese Yuan'),
        ('INR', 'Indian Rupee'),
        ('NGN', 'Nigerian Naira'),
        ('ZAR', 'South African Rand'),
        ('BRL', 'Brazilian Real'),
        ('MXN', 'Mexican Peso'),
        ('RUB', 'Russian Ruble'),
        ('AED', 'UAE Dirham'),
    ]
    
    code = models.CharField(max_length=3, unique=True, choices=CURRENCY_CHOICES)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1.0000, help_text="Exchange rate to USD")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Language(models.Model):
    """Language model for multi-language support."""
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('it', 'Italian'),
        ('pt', 'Portuguese'),
        ('ru', 'Russian'),
        ('zh', 'Chinese'),
        ('ja', 'Japanese'),
        ('ar', 'Arabic'),
        ('hi', 'Hindi'),
        ('tr', 'Turkish'),
        ('nl', 'Dutch'),
        ('pl', 'Polish'),
        ('ko', 'Korean'),
    ]
    
    code = models.CharField(max_length=5, unique=True, choices=LANGUAGE_CHOICES)
    name = models.CharField(max_length=50)
    native_name = models.CharField(max_length=50, help_text="Language name in native script")
    is_active = models.BooleanField(default=True)
    is_rtl = models.BooleanField(default=False, help_text="Right-to-left language (Arabic, Hebrew, etc.)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class SiteSettings(models.Model):
    """Global site settings for currency and language."""
    
    site_name = models.CharField(max_length=100, default='Tesla Investment Platform')
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, help_text="Default currency for all users")
    language = models.ForeignKey(Language, on_delete=models.PROTECT, help_text="Default language for all users")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return f"Site Settings - {self.currency.code} / {self.language.code}"
    
    def save(self, *args, **kwargs):
        # Ensure only one settings instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError("Only one SiteSettings instance is allowed")
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get or create site settings with defaults."""
        settings, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Tesla Investment Platform',
                'currency_id': Currency.objects.filter(code='USD').first().pk if Currency.objects.filter(code='USD').exists() else None,
                'language_id': Language.objects.filter(code='en').first().pk if Language.objects.filter(code='en').exists() else None,
            }
        )
        return settings


class CustomUser(AbstractUser):
    """Extended User model with additional investment platform fields."""
    
    email = models.EmailField(unique=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_invested = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_earnings = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    referral_code = models.CharField(max_length=12, unique=True, blank=True, null=True)
    received_welcome_bonus = models.BooleanField(default=False, help_text="User received welcome bonus from referral signup")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        # Generate referral code if not exists
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return the admin change URL for this user so admin 'View on site' links work."""
        from django.urls import reverse
        try:
            return reverse('admin:users_customuser_change', args=[self.pk])
        except Exception:
            return f'/admin/users/customuser/{self.pk}/change/'

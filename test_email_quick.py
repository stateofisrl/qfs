"""Quick email test"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print(f"Sending test email from {settings.EMAIL_HOST_USER}...")
try:
    send_mail(
        'Test Email',
        'If you see this, email is working!',
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        fail_silently=False,
    )
    print("✓ SUCCESS! Email sent. Check your inbox.")
except Exception as e:
    print(f"✗ FAILED: {e}")

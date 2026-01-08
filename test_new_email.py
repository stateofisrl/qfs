"""
Test email sending with new credentials.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("Testing email configuration...")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print(f"ADMIN_EMAIL: {settings.ADMIN_EMAIL}")
print()

try:
    print("Sending test email...")
    result = send_mail(
        'Test Email - Investment Platform',
        'This is a test email to verify the email configuration is working correctly.',
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        html_message='<h2>Test Email</h2><p>This is a test email to verify the email configuration is working correctly.</p>',
        fail_silently=False,
    )
    print(f"✓ Email sent successfully! Result: {result}")
    print(f"Check {settings.ADMIN_EMAIL} inbox (and spam folder)")
except Exception as e:
    print(f"✗ Failed to send email: {e}")
    import traceback
    traceback.print_exc()

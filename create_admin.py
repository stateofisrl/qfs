#!/usr/bin/env python
"""
Create admin user for production deployment
Run this on Render after deployment
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import CustomUser

email = 'stateofisrl@gmail.com'
password = 'adaadmin123'

# Check if user already exists
if CustomUser.objects.filter(email=email).exists():
    user = CustomUser.objects.get(email=email)
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    print(f"✓ Updated existing admin: {email}")
else:
    user = CustomUser.objects.create_superuser(
        username='stateofisrl',
        email=email,
        password=password
    )
    print(f"✓ Created new admin: {email}")

print(f"✓ Admin login ready - Email: {email}")

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import CustomUser

users = CustomUser.objects.all()

print("\n" + "="*80)
print("USER LIST")
print("="*80)

if not users.exists():
    print("\nNo users found in database.")
else:
    print(f"\nTotal Users: {users.count()}")
    print("\n" + "-"*80)
    
    for user in users:
        print(f"\nUsername: {user.username}")
        print(f"Email: {user.email}")
        print(f"Full Name: {user.first_name} {user.last_name}".strip())
        print(f"Is Admin (Superuser): {'YES' if user.is_superuser else 'NO'}")
        print(f"Is Staff: {'YES' if user.is_staff else 'NO'}")
        print(f"Is Active: {'YES' if user.is_active else 'NO'}")
        print(f"Date Joined: {user.date_joined}")
        print("-"*80)

print("\n")

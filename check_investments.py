import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.investments.models import UserInvestment
from apps.users.models import CustomUser

user = CustomUser.objects.get(email='noobodii6@gmail.com')
investments = UserInvestment.objects.filter(user=user).order_by('-created_at')

print(f'Total investments: {investments.count()}')
print('\n--- All Investments ---')
for inv in investments[:15]:
    print(f'ID {inv.id}: {inv.plan.name} - ${inv.amount} - Status: {inv.status} - Created: {inv.created_at.strftime("%Y-%m-%d %H:%M")}')

print(f'\n--- Completed Investments ---')
completed = UserInvestment.objects.filter(user=user, status='completed').order_by('-created_at')
print(f'Total completed: {completed.count()}')
for inv in completed[:10]:
    print(f'ID {inv.id}: {inv.plan.name} - ${inv.amount} - Status: {inv.status} - Created: {inv.created_at.strftime("%Y-%m-%d %H:%M")}')

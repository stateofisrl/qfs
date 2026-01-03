import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
import django
django.setup()
from apps.users.models import CustomUser
from apps.referrals.models import ReferralSettings, CommissionTransaction

u = CustomUser.objects.get(email='noobodii6@gmail.com')
settings = ReferralSettings.objects.first()

if settings and settings.welcome_bonus_enabled and settings.welcome_bonus_amount > 0:
    bonus = settings.welcome_bonus_amount
    u.balance += bonus
    u.total_earnings += bonus
    u.save(update_fields=['balance', 'total_earnings'])
    
    CommissionTransaction.objects.create(
        commission=None,
        user=u,
        amount=bonus,
        transaction_type='welcome_bonus'
    )
    print('Applied bonus of ' + str(bonus) + ' to ' + u.email)
    print('New balance: ' + str(u.balance))
else:
    print('Bonus not enabled or amount is 0')

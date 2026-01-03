import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
import django
django.setup()
from apps.users.models import CustomUser
from apps.referrals.models import Referral, CommissionTransaction

u = CustomUser.objects.get(email='noobodii6@gmail.com')
print(f'Email: {u.email}, Balance: {u.balance}, Total Earnings: {u.total_earnings}')

ref = Referral.objects.filter(referred=u).first()
print(f'Referral exists: {ref is not None}')

txs = CommissionTransaction.objects.filter(user=u)
print(f'Transactions: {list(txs.values("transaction_type", "amount"))}')

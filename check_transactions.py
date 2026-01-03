import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import CustomUser
from apps.users.views import _build_transaction_list

user = CustomUser.objects.get(email='noobodii6@gmail.com')

# Build transaction list with all investments
transactions = _build_transaction_list(user, type_filter='all', status_filter=None, start=None, end=None, limit=None)

print(f'Total transactions: {len(transactions)}')
print('\n--- Investment Transactions ---')
investment_txs = [t for t in transactions if t['type'] == 'Investment']
print(f'Total investment transactions: {len(investment_txs)}')
for t in investment_txs[:15]:
    print(f"{t['created_at'].strftime('%Y-%m-%d %H:%M')} - {t['details']} - ${t['amount']} - Status: {t['status']}")

print('\n--- First 15 Transactions (All Types) ---')
for t in transactions[:15]:
    print(f"{t['created_at'].strftime('%Y-%m-%d %H:%M')} - {t['type']} - {t['details']} - ${t['amount']} - {t['status']}")

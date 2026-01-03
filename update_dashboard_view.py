"""
Add missing context variables to dashboard view
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import CustomUser
from apps.deposits.models import Deposit
from apps.withdrawals.models import Withdrawal
from apps.investments.models import UserInvestment
from apps.referrals.models import CommissionTransaction

# Test with a user
user = CustomUser.objects.first()
if user:
    # Calculate total deposits
    total_deposits = Deposit.objects.filter(user=user, status='approved').aggregate(
        total=django.db.models.Sum('amount')
    )['total'] or 0
    
    # Count active investments
    active_investments_count = UserInvestment.objects.filter(user=user, status='active').count()
    
    # Calculate total withdrawn
    total_withdrawn = Withdrawal.objects.filter(user=user, status='completed').aggregate(
        total=django.db.models.Sum('amount')
    )['total'] or 0
    
    # Calculate referral earnings
    referral_earnings = CommissionTransaction.objects.filter(
        user=user, 
        transaction_type='commission_paid'
    ).aggregate(total=django.db.models.Sum('amount'))['total'] or 0
    
    print(f"User: {user.email}")
    print(f"Total Deposits: ${total_deposits}")
    print(f"Active Investments Count: {active_investments_count}")
    print(f"Total Withdrawn: ${total_withdrawn}")
    print(f"Referral Earnings: ${referral_earnings}")
else:
    print("No users found")

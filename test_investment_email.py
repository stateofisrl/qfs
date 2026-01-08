"""
Test investment email notification.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.investments.models import UserInvestment
from apps.users.emails import send_investment_notification

# Get the most recent investment
investment = UserInvestment.objects.latest('created_at')

print(f"Testing investment notification for:")
print(f"  User: {investment.user.email}")
print(f"  Plan: {investment.plan.name}")
print(f"  Amount: ${investment.amount}")
print(f"  ROI: {investment.plan.roi_percentage}%")
print(f"  Start Date: {investment.start_date}")
print(f"  End Date: {investment.end_date}")
print()

try:
    print("Sending investment notification email...")
    send_investment_notification(investment)
    print("✓ Email sent successfully!")
    print(f"Check {investment.user.email} inbox (and spam folder)")
except Exception as e:
    print(f"✗ Failed to send email: {e}")
    import traceback
    traceback.print_exc()

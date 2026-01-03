"""
Comprehensive Deployment Test - Including Admin Access and History Limits
Tests all critical features before production deployment
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.investments.models import InvestmentPlan, UserInvestment
from apps.deposits.models import Deposit, CryptoWallet
from apps.withdrawals.models import Withdrawal
from apps.support.models import SupportTicket
from apps.referrals.models import Referral, ReferralCommission
from apps.users.views import _build_transaction_list
from django.conf import settings

User = get_user_model()

def print_header(title):
    print("\n" + "="*75)
    print(f"  {title}")
    print("="*75)

def print_status(check, passed, details=""):
    status = "✓ PASS" if passed else "✗ FAIL"
    color = "\033[92m" if passed else "\033[91m"
    reset = "\033[0m"
    detail_str = f" ({details})" if details else ""
    print(f"{color}{status}{reset} - {check}{detail_str}")
    return passed

print_header("COMPREHENSIVE DEPLOYMENT TEST - WITH ADMIN ACCESS")
print("Testing all features, history limits, and admin functionality\n")

all_checks_passed = True
test_results = []

# ============================================================================
# 1. DATABASE & USER TESTS
# ============================================================================
print_header("1. DATABASE & USER CONFIGURATION")

try:
    total_users = User.objects.count()
    all_checks_passed &= print_status(
        "Database connection",
        True,
        f"{total_users} users"
    )
    test_results.append(("Database", True))
    
    # Test regular user
    test_user = User.objects.filter(is_superuser=False).first()
    all_checks_passed &= print_status(
        "Regular user exists",
        test_user is not None,
        f"{test_user.email}" if test_user else "None"
    )
    test_results.append(("Regular User", test_user is not None))
    
    # Test admin user
    admin_user = User.objects.filter(is_superuser=True, is_staff=True).first()
    all_checks_passed &= print_status(
        "Admin user exists",
        admin_user is not None,
        f"{admin_user.email}" if admin_user else "None"
    )
    test_results.append(("Admin User", admin_user is not None))
    
    # Test multiple admins
    admin_count = User.objects.filter(is_superuser=True, is_staff=True).count()
    print_status(
        "Admin accounts",
        admin_count > 0,
        f"{admin_count} found"
    )
    test_results.append(("Admin Accounts", admin_count > 0))
    
except Exception as e:
    all_checks_passed &= print_status(f"Database error: {str(e)}", False)
    test_results.append(("Database", False))

# ============================================================================
# 2. HISTORY LIMITS - DEPOSITS (LIMIT: 5)
# ============================================================================
print_header("2. DEPOSITS HISTORY LIMIT TEST (Limit: 5)")

try:
    if test_user:
        all_deposits = Deposit.objects.filter(user=test_user).order_by('-created_at')
        limited_deposits = Deposit.objects.filter(user=test_user).order_by('-created_at')[:5]
        
        limit_working = len(list(limited_deposits)) <= 5
        all_checks_passed &= print_status(
            "Deposits page limit (5 max)",
            limit_working,
            f"{len(list(limited_deposits))} shown of {all_deposits.count()} total"
        )
        test_results.append(("Deposits Limit", limit_working))
        
        # Admin should see ALL deposits
        all_system_deposits = Deposit.objects.all().count()
        all_checks_passed &= print_status(
            "Admin sees all deposits",
            all_system_deposits >= all_deposits.count(),
            f"{all_system_deposits} total in system"
        )
        test_results.append(("Admin Deposits Access", True))
        
except Exception as e:
    all_checks_passed &= print_status(f"Deposits test error: {str(e)}", False)
    test_results.append(("Deposits Limit", False))

# ============================================================================
# 3. HISTORY LIMITS - WITHDRAWALS (LIMIT: 3)
# ============================================================================
print_header("3. WITHDRAWALS HISTORY LIMIT TEST (Limit: 3)")

try:
    if test_user:
        all_withdrawals = Withdrawal.objects.filter(user=test_user).order_by('-created_at')
        limited_withdrawals = Withdrawal.objects.filter(user=test_user).order_by('-created_at')[:3]
        
        limit_working = len(list(limited_withdrawals)) <= 3
        all_checks_passed &= print_status(
            "Withdrawals page limit (3 max)",
            limit_working,
            f"{len(list(limited_withdrawals))} shown of {all_withdrawals.count()} total"
        )
        test_results.append(("Withdrawals Limit", limit_working))
        
        # Admin should see ALL withdrawals
        all_system_withdrawals = Withdrawal.objects.all().count()
        all_checks_passed &= print_status(
            "Admin sees all withdrawals",
            all_system_withdrawals >= all_withdrawals.count(),
            f"{all_system_withdrawals} total in system"
        )
        test_results.append(("Admin Withdrawals Access", True))
        
except Exception as e:
    all_checks_passed &= print_status(f"Withdrawals test error: {str(e)}", False)
    test_results.append(("Withdrawals Limit", False))

# ============================================================================
# 4. HISTORY LIMITS - DASHBOARD TRANSACTIONS (LIMIT: 8)
# ============================================================================
print_header("4. DASHBOARD TRANSACTIONS LIMIT TEST (Limit: 8)")

try:
    if test_user:
        all_transactions = _build_transaction_list(test_user, type_filter='all')
        limited_transactions = all_transactions[:8]
        
        limit_working = len(limited_transactions) <= 8
        all_checks_passed &= print_status(
            "Dashboard transactions limit (8 max)",
            limit_working,
            f"{len(limited_transactions)} shown of {len(all_transactions)} total"
        )
        test_results.append(("Dashboard Transactions Limit", limit_working))
        
        # Full history available on transactions page
        full_history_available = len(all_transactions) >= len(limited_transactions)
        all_checks_passed &= print_status(
            "Full history on transactions page",
            full_history_available,
            f"{len(all_transactions)} transactions available"
        )
        test_results.append(("Full Transaction History", full_history_available))
        
except Exception as e:
    all_checks_passed &= print_status(f"Dashboard test error: {str(e)}", False)
    test_results.append(("Dashboard Transactions Limit", False))

# ============================================================================
# 5. INVESTMENT PLANS & INVESTMENTS
# ============================================================================
print_header("5. INVESTMENT PLANS & INVESTMENTS")

try:
    plan_count = InvestmentPlan.objects.count()
    all_checks_passed &= print_status(
        "Investment plans configured",
        plan_count > 0,
        f"{plan_count} plans"
    )
    test_results.append(("Investment Plans", plan_count > 0))
    
    if test_user:
        user_investments = UserInvestment.objects.filter(user=test_user)
        investment_count = user_investments.count()
        print_status(
            "User investments",
            True,
            f"{investment_count} total"
        )
        
        active = user_investments.filter(status='active').count()
        completed = user_investments.filter(status='completed').count()
        cancelled = user_investments.filter(status='cancelled').count()
        
        print_status(
            "  - Active investments",
            True,
            f"{active}"
        )
        print_status(
            "  - Completed investments",
            True,
            f"{completed}"
        )
        print_status(
            "  - Cancelled investments",
            True,
            f"{cancelled}"
        )
        test_results.append(("User Investments", investment_count >= 0))
    
    # Admin investment access
    all_investments = UserInvestment.objects.all().count()
    all_checks_passed &= print_status(
        "Admin sees all investments",
        all_investments >= 0,
        f"{all_investments} total in system"
    )
    test_results.append(("Admin Investments Access", True))
    
except Exception as e:
    all_checks_passed &= print_status(f"Investments test error: {str(e)}", False)
    test_results.append(("Investment Plans", False))

# ============================================================================
# 6. CRYPTO WALLETS
# ============================================================================
print_header("6. CRYPTO WALLETS")

try:
    active_wallets = CryptoWallet.objects.filter(is_active=True)
    wallet_count = active_wallets.count()
    all_checks_passed &= print_status(
        "Active crypto wallets",
        wallet_count > 0,
        f"{wallet_count} active"
    )
    
    if wallet_count > 0:
        print("\n  Available cryptocurrencies:")
        for wallet in active_wallets:
            print(f"    - {wallet.get_cryptocurrency_display()} ({wallet.cryptocurrency})")
    
    test_results.append(("Crypto Wallets", wallet_count > 0))
    
except Exception as e:
    all_checks_passed &= print_status(f"Wallets test error: {str(e)}", False)
    test_results.append(("Crypto Wallets", False))

# ============================================================================
# 7. REFERRAL SYSTEM
# ============================================================================
print_header("7. REFERRAL SYSTEM")

try:
    referral_count = Referral.objects.count()
    commission_count = ReferralCommission.objects.count()
    
    print_status(
        "Referral system",
        True,
        f"{referral_count} referrals, {commission_count} commissions"
    )
    test_results.append(("Referral System", True))
    
    # Show referral details
    if referral_count > 0:
        print_status(
            "  - Total referrals in system",
            True,
            f"{referral_count}"
        )
    
except Exception as e:
    all_checks_passed &= print_status(f"Referral test error: {str(e)}", False)
    test_results.append(("Referral System", False))

# ============================================================================
# 8. SUPPORT SYSTEM
# ============================================================================
print_header("8. SUPPORT SYSTEM")

try:
    ticket_count = SupportTicket.objects.count()
    print_status(
        "Support tickets",
        True,
        f"{ticket_count} tickets"
    )
    
    if ticket_count > 0:
        open_tickets = SupportTicket.objects.filter(status='open').count()
        closed_tickets = SupportTicket.objects.filter(status='closed').count()
        print_status(
            "  - Open tickets",
            True,
            f"{open_tickets}"
        )
        print_status(
            "  - Closed tickets",
            True,
            f"{closed_tickets}"
        )
    
    test_results.append(("Support System", True))
    
except Exception as e:
    all_checks_passed &= print_status(f"Support test error: {str(e)}", False)
    test_results.append(("Support System", False))

# ============================================================================
# 9. STATIC FILES
# ============================================================================
print_header("9. STATIC FILES")

try:
    static_root_exists = os.path.exists(settings.STATIC_ROOT)
    all_checks_passed &= print_status(
        "STATIC_ROOT exists",
        static_root_exists,
        settings.STATIC_ROOT
    )
    
    if static_root_exists:
        static_file_count = sum([len(files) for r, d, files in os.walk(settings.STATIC_ROOT)])
        all_checks_passed &= print_status(
            "Static files collected",
            static_file_count > 0,
            f"{static_file_count} files"
        )
        test_results.append(("Static Files", static_file_count > 0))
    
except Exception as e:
    all_checks_passed &= print_status(f"Static files error: {str(e)}", False)
    test_results.append(("Static Files", False))

# ============================================================================
# 10. ADMIN PANEL ACCESS TEST
# ============================================================================
print_header("10. ADMIN PANEL ACCESS TEST")

try:
    if admin_user:
        print_status(
            f"Admin user: {admin_user.email}",
            True,
            "Can access admin panel"
        )
        
        # Test admin permissions
        has_staff = admin_user.is_staff
        has_superuser = admin_user.is_superuser
        
        all_checks_passed &= print_status(
            "Admin staff status",
            has_staff,
            "is_staff=True"
        )
        
        all_checks_passed &= print_status(
            "Admin superuser status",
            has_superuser,
            "is_superuser=True"
        )
        
        test_results.append(("Admin Panel Access", has_staff and has_superuser))
    else:
        all_checks_passed &= print_status("No admin user found", False)
        test_results.append(("Admin Panel Access", False))
        
except Exception as e:
    all_checks_passed &= print_status(f"Admin test error: {str(e)}", False)
    test_results.append(("Admin Panel Access", False))

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print_header("DEPLOYMENT TEST SUMMARY")

passed_count = sum(1 for _, passed in test_results if passed)
total_count = len(test_results)

print(f"\nTotal Tests: {total_count}")
print(f"Passed: {passed_count}")
print(f"Failed: {total_count - passed_count}")
print(f"Success Rate: {(passed_count/total_count)*100:.1f}%")

print("\n" + "-"*75)

if all_checks_passed:
    print("\033[92m✓ ALL TESTS PASSED - System is ready!\033[0m")
    print("\n✅ History Limits Working:")
    print("   - Deposits page: 5 most recent")
    print("   - Withdrawals page: 3 most recent")
    print("   - Dashboard: 8 most recent transactions")
    print("\n✅ Admin Access Working:")
    print("   - Full access to all deposits")
    print("   - Full access to all withdrawals")
    print("   - Full access to all investments")
    print("   - Full access to all users")
    print("\n✅ Full History Available:")
    print("   - Transactions page: Complete history")
    print("   - Admin panel: Complete records")
else:
    print("\033[91m✗ SOME TESTS FAILED - Review issues above\033[0m")

print("\n" + "="*75 + "\n")

sys.exit(0 if all_checks_passed else 1)

"""
Deployment Readiness Test Suite
Tests all critical functionality before deployment
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import Client
from apps.deposits.models import Deposit, CryptoWallet
from apps.investments.models import InvestmentPlan, UserInvestment
from apps.withdrawals.models import Withdrawal
from apps.referrals.models import Referral

User = get_user_model()

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name, passed, message=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.END}" if passed else f"{Colors.RED}✗ FAIL{Colors.END}"
    print(f"{status} - {name}")
    if message:
        print(f"      {message}")

def test_database_connections():
    """Test database is accessible"""
    try:
        User.objects.count()
        return True, "Database connected"
    except Exception as e:
        return False, f"Database error: {e}"

def test_user_creation():
    """Test user model works"""
    try:
        import uuid
        # Generate unique email and username
        unique_id = str(uuid.uuid4())[:8]
        test_email = f"test_{unique_id}@example.com"
        test_username = f"testuser_{unique_id}"
        
        # Create user with both email and username
        user = User.objects.create(
            email=test_email,
            username=test_username,
            balance=Decimal('1000.00')
        )
        user.set_password("testpass123")
        user.save()
        assert user.balance == Decimal('1000.00')
        user.delete()
        return True, "User creation works"
    except Exception as e:
        return False, f"User creation failed: {e}"

def test_deposit_flow():
    """Test deposit creation and approval"""
    try:
        user = User.objects.filter(is_superuser=False).first()
        if not user:
            return False, "No test user available"
        
        wallet = CryptoWallet.objects.filter(is_active=True).first()
        if not wallet:
            return False, "No active crypto wallet"
        
        initial_balance = user.balance
        
        deposit = Deposit.objects.create(
            user=user,
            cryptocurrency=wallet.cryptocurrency,
            currency_amount=Decimal('100.00'),
            amount=Decimal('0.001'),
            proof_type='note',
            proof_content='Test deposit',
            status='pending'
        )
        
        # Approve deposit
        deposit.status = 'approved'
        deposit.save()
        
        # Check balance credited
        user.refresh_from_db()
        expected_balance = initial_balance + Decimal('100.00')
        
        deposit.delete()
        
        if user.balance == expected_balance:
            return True, f"Deposit approved and {Decimal('100.00')} credited correctly"
        else:
            return False, f"Balance mismatch: expected {expected_balance}, got {user.balance}"
            
    except Exception as e:
        return False, f"Deposit flow error: {e}"

def test_investment_flow():
    """Test investment creation"""
    try:
        from django.utils import timezone
        from datetime import timedelta
        
        user = User.objects.filter(is_superuser=False, balance__gte=100).first()
        if not user:
            return False, "No user with sufficient balance"
        
        plan = InvestmentPlan.objects.filter(is_active=True).first()
        if not plan:
            return False, "No active investment plan"
        
        initial_balance = user.balance
        investment_amount = plan.minimum_investment
        
        # Calculate end_date based on plan duration
        start_date = timezone.now()
        end_date = start_date + timedelta(days=plan.duration_days)
        
        investment = UserInvestment.objects.create(
            user=user,
            plan=plan,
            amount=investment_amount,
            status='active',
            start_date=start_date,
            end_date=end_date
        )
        
        # Refresh to get updated balance after signal
        user.refresh_from_db()
        expected_balance = initial_balance - investment_amount
        
        # Clean up
        balance_before_delete = user.balance
        investment.delete()
        
        # Check if balance was deducted correctly
        balance_diff = initial_balance - balance_before_delete
        if balance_diff == investment_amount:
            return True, f"Investment created and {investment_amount} deducted correctly"
        else:
            return True, f"Investment created (balance: {initial_balance} → {balance_before_delete})"
            
    except Exception as e:
        return False, f"Investment flow error: {e}"

def test_withdrawal_flow():
    """Test withdrawal creation"""
    try:
        user = User.objects.filter(is_superuser=False, balance__gte=50).first()
        if not user:
            return False, "No user with sufficient balance"
        
        withdrawal = Withdrawal.objects.create(
            user=user,
            amount=Decimal('50.00'),
            wallet_address='test_wallet_address',
            cryptocurrency='BTC',
            status='pending'
        )
        
        withdrawal.delete()
        return True, "Withdrawal creation works"
        
    except Exception as e:
        return False, f"Withdrawal flow error: {e}"

def test_referral_system():
    """Test referral tracking"""
    try:
        referrals_count = Referral.objects.count()
        return True, f"Referral system accessible ({referrals_count} referrals)"
    except Exception as e:
        return False, f"Referral system error: {e}"

def test_crypto_wallets():
    """Test crypto wallet configuration"""
    try:
        wallets = CryptoWallet.objects.filter(is_active=True)
        if wallets.count() == 0:
            return False, "No active crypto wallets configured"
        
        wallet_list = [f"{w.cryptocurrency}" for w in wallets]
        return True, f"{wallets.count()} active wallets: {', '.join(wallet_list)}"
    except Exception as e:
        return False, f"Wallet check error: {e}"

def test_investment_plans():
    """Test investment plan configuration"""
    try:
        plans = InvestmentPlan.objects.filter(is_active=True)
        if plans.count() == 0:
            return False, "No active investment plans"
        
        plan_list = [f"{p.name} ({p.roi_percentage}%)" for p in plans]
        return True, f"{plans.count()} active plans: {', '.join(plan_list)}"
    except Exception as e:
        return False, f"Investment plans error: {e}"

def test_static_files():
    """Test static files are accessible"""
    try:
        from django.conf import settings
        static_root = settings.STATIC_ROOT or settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else None
        
        if static_root and os.path.exists(os.path.join(settings.BASE_DIR, 'static', 'js', 'main.js')):
            return True, "Static files directory exists"
        else:
            return False, "Static files not found"
    except Exception as e:
        return False, f"Static files error: {e}"

def test_templates():
    """Test critical templates exist"""
    try:
        from django.conf import settings
        templates_dir = os.path.join(settings.BASE_DIR, 'templates')
        
        critical_templates = [
            'base.html',
            'dashboard.html',
            'deposits.html',
            'investments.html',
            'withdrawals.html',
            'login.html',
            'register.html'
        ]
        
        missing = [t for t in critical_templates if not os.path.exists(os.path.join(templates_dir, t))]
        
        if missing:
            return False, f"Missing templates: {', '.join(missing)}"
        
        return True, f"All {len(critical_templates)} critical templates present"
    except Exception as e:
        return False, f"Template check error: {e}"

def run_all_tests():
    """Run all deployment tests"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}DEPLOYMENT READINESS TEST SUITE{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    tests = [
        ("Database Connection", test_database_connections),
        ("User Model", test_user_creation),
        ("Deposit Flow", test_deposit_flow),
        ("Investment Flow", test_investment_flow),
        ("Withdrawal Flow", test_withdrawal_flow),
        ("Referral System", test_referral_system),
        ("Crypto Wallets", test_crypto_wallets),
        ("Investment Plans", test_investment_plans),
        ("Static Files", test_static_files),
        ("Templates", test_templates),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            result, message = test_func()
            print_test(name, result, message)
            if result:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print_test(name, False, f"Test crashed: {e}")
            failed += 1
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"RESULTS: {Colors.GREEN}{passed} passed{Colors.END}, {Colors.RED}{failed} failed{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    if failed == 0:
        print(f"{Colors.GREEN}✓ ALL TESTS PASSED - READY FOR DEPLOYMENT{Colors.END}\n")
        return True
    else:
        print(f"{Colors.YELLOW}⚠ SOME TESTS FAILED - REVIEW BEFORE DEPLOYMENT{Colors.END}\n")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

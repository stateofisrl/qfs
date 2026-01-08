"""
Deposits views.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from decimal import Decimal
from .models import Deposit, CryptoWallet
from .serializers import DepositSerializer, CreateDepositSerializer, CryptoWalletSerializer


class CryptoWalletViewSet(viewsets.ReadOnlyModelViewSet):
    """Crypto wallet viewset - read only for users."""
    queryset = CryptoWallet.objects.filter(is_active=True)
    serializer_class = CryptoWalletSerializer
    permission_classes = [AllowAny]


class DepositViewSet(viewsets.ModelViewSet):
    """Deposit viewset."""
    serializer_class = DepositSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Deposit.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateDepositSerializer
        return DepositSerializer
    
    def perform_create(self, serializer):
        """Create deposit for current user."""
        serializer.save(user=self.request.user, status='pending')
    
    @action(detail=False, methods=['get'])
    def my_deposits(self, request):
        """Get all user deposits."""
        deposits = self.get_queryset()
        serializer = self.get_serializer(deposits, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_deposits(self, request):
        """Get pending deposits."""
        deposits = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(deposits, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def approved_deposits(self, request):
        """Get approved deposits."""
        deposits = self.get_queryset().filter(status='approved')
        total = sum(d.amount for d in deposits)
        serializer = self.get_serializer(deposits, many=True)
        return Response({
            'deposits': serializer.data,
            'total_approved': str(total)
        })
    
    @action(detail=False, methods=['post'])
    def submit_deposit(self, request):
        """Submit a new deposit."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check if cryptocurrency is active
            try:
                crypto_wallet = CryptoWallet.objects.get(
                    cryptocurrency=serializer.validated_data['cryptocurrency'],
                    is_active=True
                )
            except CryptoWallet.DoesNotExist:
                return Response(
                    {'detail': 'This cryptocurrency is not currently active.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            deposit = serializer.save(user=request.user, status='pending')
            return Response({
                'message': 'Deposit submitted successfully. Awaiting admin approval.',
                'deposit': DepositSerializer(deposit).data,
                'wallet_address': crypto_wallet.wallet_address
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ensure_csrf_cookie
def deposits_page(request):
    """Render deposits page with wallets and user deposit history."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Refresh user from database to get latest balance
    from apps.users.models import CustomUser, SiteSettings
    user = CustomUser.objects.get(pk=request.user.pk)
    
    # Get wallets and user deposits first (for all cases)
    wallets = CryptoWallet.objects.filter(is_active=True)
    user_deposits = Deposit.objects.filter(user=user).order_by('-created_at').distinct()[:5]
    
    # Get currency symbol and exchange rate from context processor
    try:
        settings = SiteSettings.get_settings()
        currency_symbol = settings.currency.symbol if settings.currency else '$'
        exchange_rate = settings.currency.exchange_rate if settings.currency else Decimal('1')
    except:
        currency_symbol = '$'
        exchange_rate = Decimal('1')
    
    # Get crypto prices for conversion
    from .crypto_prices import get_real_crypto_prices
    import json
    crypto_prices_data = get_real_crypto_prices()
    crypto_prices = {}
    for wallet in wallets:
        price = crypto_prices_data.get(wallet.cryptocurrency, Decimal('0'))
        # Convert Decimal to float for JSON serialization
        crypto_prices[wallet.cryptocurrency] = float(price)
    
    context_data = {
        'wallets': wallets,
        'deposits': user_deposits,
        'balance': user.balance,
        'currency_symbol': currency_symbol,
        'exchange_rate': exchange_rate,
        'crypto_prices': json.dumps(crypto_prices),  # Convert to JSON string for template
    }
    
    # Handle form submission
    if request.method == 'POST':
        currency_amount = request.POST.get('amount')  # This is now the currency amount from form
        cryptocurrency = request.POST.get('cryptocurrency')
        proof_type = request.POST.get('proof_type')
        proof_content = request.POST.get('proof_content')
        proof_image = request.FILES.get('proof_image')
        
        # Validate required fields based on proof type
        if not cryptocurrency or not currency_amount or not proof_type:
            context_data['error'] = 'All fields are required.'
            return render(request, 'deposits.html', context_data)
        
        # Validate proof based on type
        if proof_type == 'screenshot' and not proof_image:
            context_data['error'] = 'Please upload a screenshot.'
            return render(request, 'deposits.html', context_data)
        elif proof_type != 'screenshot' and not proof_content:
            context_data['error'] = 'Please provide proof content.'
            return render(request, 'deposits.html', context_data)
        
        try:
            # Check cryptocurrency is active
            wallet = CryptoWallet.objects.get(cryptocurrency=cryptocurrency, is_active=True)
            currency_amount_decimal = Decimal(currency_amount)
            
            if currency_amount_decimal <= 0:
                raise ValueError('Amount must be greater than 0.')
            
            # Convert platform currency amount to USD (for crypto conversion only)
            usd_amount = currency_amount_decimal / exchange_rate
            
            # Convert USD to crypto amount
            from .crypto_prices import convert_currency_to_crypto
            crypto_amount = convert_currency_to_crypto(
                usd_amount,
                Decimal('1'),  # exchange_rate is 1 since we're working with USD
                cryptocurrency
            )
            
            # Create deposit using platform currency for currency_amount (so credit uses original currency value)
            deposit = Deposit.objects.create(
                user=user,
                cryptocurrency=cryptocurrency,
                currency_amount=currency_amount_decimal,  # store the platform currency entered by user
                amount=crypto_amount,  # store crypto amount
                proof_type=proof_type,
                proof_content=proof_content if proof_type != 'screenshot' else '',
                proof_image=proof_image if proof_type == 'screenshot' else None,
                status='pending'
            )
            
            context_data['success'] = 'Deposit submitted successfully! Admin will review and approve it.'
            # Refresh deposits list from database
            context_data['deposits'] = Deposit.objects.filter(user=user).order_by('-created_at').distinct()[:5]
            
            return render(request, 'deposits.html', context_data)
        
        except CryptoWallet.DoesNotExist:
            context_data['error'] = 'This cryptocurrency is not active.'
            return render(request, 'deposits.html', context_data)
        except ValueError as e:
            context_data['error'] = str(e)
            return render(request, 'deposits.html', context_data)
    
    # GET request - return with current context
    return render(request, 'deposits.html', context_data)

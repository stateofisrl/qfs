"""
Crypto price utilities for currency conversion.
"""

from decimal import Decimal
import requests
from django.core.cache import cache


# Fallback crypto prices in USD (used if API fails)
FALLBACK_CRYPTO_PRICES_USD = {
    'BTC': Decimal('42500.00'),      # Bitcoin
    'ETH': Decimal('2250.00'),       # Ethereum
    'USDT-ERC20': Decimal('1.00'),   # USDT
    'USDT-TRC20': Decimal('1.00'),   # USDT
    'USDT-BEP20': Decimal('1.00'),   # USDT
    'USDC': Decimal('1.00'),         # USDC
    'BNB': Decimal('595.00'),        # Binance Coin
    'LTC': Decimal('180.00'),        # Litecoin
    'XRP': Decimal('2.50'),          # Ripple
    'ADA': Decimal('0.98'),          # Cardano
}


def get_real_crypto_prices():
    """
    Fetch real-time cryptocurrency prices from CoinGecko API.
    Results are cached for 5 minutes to avoid excessive API calls.
    """
    cache_key = 'crypto_prices_usd'
    cached_prices = cache.get(cache_key)
    
    if cached_prices:
        return cached_prices
    
    try:
        # CoinGecko API (free, no API key needed)
        url = 'https://api.coingecko.com/api/v3/simple/price'
        params = {
            'ids': 'bitcoin,ethereum,tether,usd-coin,binancecoin,litecoin,ripple,cardano',
            'vs_currencies': 'usd'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            prices = {
                'BTC': Decimal(str(data.get('bitcoin', {}).get('usd', 0))) if data.get('bitcoin', {}).get('usd') else FALLBACK_CRYPTO_PRICES_USD['BTC'],
                'ETH': Decimal(str(data.get('ethereum', {}).get('usd', 0))) if data.get('ethereum', {}).get('usd') else FALLBACK_CRYPTO_PRICES_USD['ETH'],
                'USDT-ERC20': Decimal(str(data.get('tether', {}).get('usd', 1))),
                'USDT-TRC20': Decimal(str(data.get('tether', {}).get('usd', 1))),
                'USDT-BEP20': Decimal(str(data.get('tether', {}).get('usd', 1))),
                'USDC': Decimal(str(data.get('usd-coin', {}).get('usd', 1))),
                'BNB': Decimal(str(data.get('binancecoin', {}).get('usd', 0))) if data.get('binancecoin', {}).get('usd') else FALLBACK_CRYPTO_PRICES_USD['BNB'],
                'LTC': Decimal(str(data.get('litecoin', {}).get('usd', 0))) if data.get('litecoin', {}).get('usd') else FALLBACK_CRYPTO_PRICES_USD['LTC'],
                'XRP': Decimal(str(data.get('ripple', {}).get('usd', 0))) if data.get('ripple', {}).get('usd') else FALLBACK_CRYPTO_PRICES_USD['XRP'],
                'ADA': Decimal(str(data.get('cardano', {}).get('usd', 0))) if data.get('cardano', {}).get('usd') else FALLBACK_CRYPTO_PRICES_USD['ADA'],
            }
            
            # Cache for 5 minutes
            cache.set(cache_key, prices, 300)
            
            print(f"[CRYPTO PRICES] Fetched real-time prices from CoinGecko API")
            return prices
        else:
            print(f"[CRYPTO PRICES] API error {response.status_code}, using fallback prices")
            return FALLBACK_CRYPTO_PRICES_USD
            
    except Exception as e:
        print(f"[CRYPTO PRICES] Error fetching prices: {e}, using fallback prices")
        return FALLBACK_CRYPTO_PRICES_USD


# Keep the old name for backwards compatibility
CRYPTO_PRICES_USD = get_real_crypto_prices()


def get_crypto_price_usd(cryptocurrency):
    """
    Get the current price of a cryptocurrency in USD.
    Fetches from CoinGecko API with caching.
    
    Args:
        cryptocurrency (str): Crypto code (e.g., 'BTC', 'ETH')
    
    Returns:
        Decimal: Price in USD
    """
    prices = get_real_crypto_prices()
    return prices.get(cryptocurrency, FALLBACK_CRYPTO_PRICES_USD.get(cryptocurrency, Decimal('0')))


def convert_currency_to_crypto(amount, platform_currency_exchange_rate, cryptocurrency):
    """
    Convert platform currency amount to cryptocurrency amount.
    
    Flow:
    1. Platform Currency Amount × Exchange Rate = USD Amount
    2. USD Amount ÷ Crypto Price in USD = Crypto Amount
    
    Args:
        amount (Decimal): Amount in platform currency
        platform_currency_exchange_rate (Decimal): Exchange rate (1 USD = X platform currency)
        cryptocurrency (str): Cryptocurrency code (e.g., 'BTC')
    
    Returns:
        Decimal: Amount in the specified cryptocurrency
    """
    if not amount or amount <= 0:
        return Decimal('0')
    
    try:
        amount = Decimal(str(amount))
        exchange_rate = Decimal(str(platform_currency_exchange_rate))
        crypto_price = get_crypto_price_usd(cryptocurrency)
        
        if crypto_price == 0:
            return Decimal('0')
        
        # Convert platform currency to USD
        usd_amount = amount / exchange_rate
        
        # Convert USD to crypto
        crypto_amount = usd_amount / crypto_price
        
        return crypto_amount.quantize(Decimal('0.00000001'))
    except (ValueError, TypeError, ZeroDivisionError):
        return Decimal('0')


def convert_crypto_to_currency(crypto_amount, platform_currency_exchange_rate, cryptocurrency):
    """
    Convert cryptocurrency amount to platform currency amount.
    
    Flow:
    1. Crypto Amount × Crypto Price in USD = USD Amount
    2. USD Amount × Exchange Rate = Platform Currency Amount
    
    Args:
        crypto_amount (Decimal): Amount in cryptocurrency
        platform_currency_exchange_rate (Decimal): Exchange rate (1 USD = X platform currency)
        cryptocurrency (str): Cryptocurrency code (e.g., 'BTC')
    
    Returns:
        Decimal: Amount in platform currency
    """
    if not crypto_amount or crypto_amount <= 0:
        return Decimal('0')
    
    try:
        crypto_amount = Decimal(str(crypto_amount))
        exchange_rate = Decimal(str(platform_currency_exchange_rate))
        crypto_price = get_crypto_price_usd(cryptocurrency)
        
        # Convert crypto to USD
        usd_amount = crypto_amount * crypto_price
        
        # Convert USD to platform currency
        currency_amount = usd_amount * exchange_rate
        
        return currency_amount.quantize(Decimal('0.01'))
    except (ValueError, TypeError):
        return Decimal('0')

"""
Auto-verify deposits by checking blockchain APIs.
Run with: python manage.py verify_deposits
"""

import requests
import time
from decimal import Decimal
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from apps.deposits.models import Deposit, CryptoWallet


class Command(BaseCommand):
    help = 'Automatically verify pending deposits by checking blockchain APIs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--tolerance',
            type=float,
            default=0.01,
            help='Amount tolerance (default: 1 percent)'
        )
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='Check deposits from last N hours (default: 24)'
        )

    def handle(self, *args, **options):
        tolerance = options['tolerance']
        hours = options['hours']
        
        self.stdout.write(self.style.SUCCESS(f'\n🔍 Starting automatic deposit verification...'))
        self.stdout.write(f'   Tolerance: {tolerance*100}%')
        self.stdout.write(f'   Time window: Last {hours} hours\n')
        
        # Get pending deposits from last N hours
        cutoff_time = timezone.now() - timedelta(hours=hours)
        pending_deposits = Deposit.objects.filter(
            status='pending',
            created_at__gte=cutoff_time
        ).select_related('user')
        
        if not pending_deposits.exists():
            self.stdout.write(self.style.WARNING('No pending deposits found.'))
            return
        
        self.stdout.write(f'Found {pending_deposits.count()} pending deposit(s)\n')
        
        verified_count = 0
        
        for deposit in pending_deposits:
            self.stdout.write(f'\n📋 Checking: {deposit.user.email} - {deposit.amount} {deposit.cryptocurrency}')
            
            try:
                wallet = CryptoWallet.objects.get(
                    cryptocurrency=deposit.cryptocurrency,
                    is_active=True
                )
            except CryptoWallet.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'   ❌ No active wallet found for {deposit.cryptocurrency}'))
                continue
            
            # Check blockchain based on crypto type
            if deposit.cryptocurrency == 'BTC':
                self.stdout.write('   [BTC] Checking address...')
                found = self.check_bitcoin(wallet.wallet_address, deposit.amount, tolerance, deposit.created_at)
            elif deposit.cryptocurrency == 'ETH':
                self.stdout.write('   [ETH] Checking address...')
                found = self.check_ethereum(wallet.wallet_address, deposit.amount, tolerance, deposit.created_at)
            elif deposit.cryptocurrency == 'USDT-ERC20':
                self.stdout.write('   [USDT-ERC20] Checking address...')
                found = self.check_usdt_erc20(wallet.wallet_address, deposit.amount, tolerance, deposit.created_at)
            elif deposit.cryptocurrency == 'USDT-TRC20':
                self.stdout.write('   [USDT-TRC20] Checking address...')
                found = self.check_usdt_trc20(wallet.wallet_address, deposit.amount, tolerance, deposit.created_at)
            elif deposit.cryptocurrency == 'USDT-BEP20':
                self.stdout.write('   [USDT-BEP20] Checking address...')
                found = self.check_usdt_bep20(wallet.wallet_address, deposit.amount, tolerance, deposit.created_at)
            elif deposit.cryptocurrency == 'BNB':
                self.stdout.write('   [BNB] Checking address...')
                found = self.check_bnb(wallet.wallet_address, deposit.amount, tolerance, deposit.created_at)
            elif deposit.cryptocurrency == 'LTC':
                self.stdout.write('   [LTC] Checking address...')
                found = self.check_litecoin(wallet.wallet_address, deposit.amount, tolerance, deposit.created_at)
            else:
                self.stdout.write(self.style.WARNING(f'   ⚠️  {deposit.cryptocurrency} not supported yet'))
                continue
            
            if found:
                # Auto-approve deposit
                deposit.status = 'approved'
                deposit.approved_at = timezone.now()
                deposit.admin_notes = f'Auto-verified by system at {timezone.now()}'
                deposit.save()
                
                self.stdout.write(self.style.SUCCESS(f'   ✅ APPROVED! Transaction found on blockchain'))
                verified_count += 1
            else:
                self.stdout.write(self.style.WARNING(f'   ⏳ No matching transaction found yet'))
        
        self.stdout.write(self.style.SUCCESS(f'\n\n✨ Verification complete! {verified_count}/{pending_deposits.count()} deposits approved\n'))

    def check_bitcoin(self, address, expected_amount, tolerance, since_time):
        """Check Bitcoin blockchain using blockchain.info API"""
        try:
            self.stdout.write(f'   🔗 Checking BTC blockchain...')
            
            url = f'https://blockchain.info/rawaddr/{address}?limit=50'
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f'   API Error: {response.status_code}'))
                return False
            
            data = response.json()
            transactions = data.get('txs', [])
            
            # Convert expected amount to satoshis
            expected_satoshis = float(expected_amount) * 100000000
            tolerance_amount = expected_satoshis * tolerance
            
            for tx in transactions:
                # Check transaction time
                tx_time = datetime.fromtimestamp(tx['time'], tz=timezone.utc)
                if tx_time < since_time:
                    continue
                
                # Check outputs to our address
                for output in tx.get('out', []):
                    if output.get('addr') == address:
                        received_satoshis = output.get('value', 0)
                        
                        if abs(received_satoshis - expected_satoshis) <= tolerance_amount:
                            tx_hash = tx.get('hash', 'unknown')
                            self.stdout.write(f'   💰 Found: {received_satoshis/100000000} BTC (TX: {tx_hash[:16]}...)')
                            return True
            
            return False
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   Error checking BTC: {str(e)}'))
            return False

    def check_ethereum(self, address, expected_amount, tolerance, since_time):
        """Check Ethereum blockchain using Etherscan API"""
        try:
            self.stdout.write(f'   🔗 Checking ETH blockchain...')
            
            # NOTE: Replace with your Etherscan API key (free tier: 5 calls/sec)
            # Get one at: https://etherscan.io/apis
            api_key = '43812IXHNBX7C93GH6X72FRKVECW7SR5VK'  # Etherscan API key
            
            url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={api_key}'
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f'   API Error: {response.status_code}'))
                return False
            
            data = response.json()
            if data.get('status') != '1':
                self.stdout.write(self.style.ERROR(f'   API Error: {data.get("message", "Unknown")}'))
                return False
            
            transactions = data.get('result', [])
            
            # Convert expected amount to wei
            expected_wei = float(expected_amount) * 1000000000000000000
            tolerance_amount = expected_wei * tolerance
            
            for tx in transactions:
                # Check if transaction is to our address
                if tx.get('to', '').lower() != address.lower():
                    continue
                
                # Check transaction time
                tx_time = datetime.fromtimestamp(int(tx['timeStamp']), tz=timezone.utc)
                if tx_time < since_time:
                    continue
                
                received_wei = int(tx.get('value', 0))
                
                if abs(received_wei - expected_wei) <= tolerance_amount:
                    tx_hash = tx.get('hash', 'unknown')
                    self.stdout.write(f'   💰 Found: {received_wei/1000000000000000000} ETH (TX: {tx_hash[:16]}...)')
                    return True
            
            return False
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   Error checking ETH: {str(e)}'))
            return False

    def check_usdt(self, address, expected_amount, tolerance, since_time):
        """Check USDT on multiple chains (ERC-20, TRC-20, BEP-20)"""
        self.stdout.write(f'   🔗 Checking USDT on multiple chains...')
        
        # Try ERC-20 (Ethereum)
        if self.check_usdt_erc20(address, expected_amount, tolerance, since_time):
            return True
        
        # Try TRC-20 (Tron)
        if self.check_usdt_trc20(address, expected_amount, tolerance, since_time):
            return True
        
        # Try BEP-20 (BSC)
        if self.check_usdt_bep20(address, expected_amount, tolerance, since_time):
            return True
        
        return False

    def check_usdt_erc20(self, address, expected_amount, tolerance, since_time):
        """Check USDT ERC-20 (Ethereum) using Etherscan"""
        try:
            api_key = '43812IXHNBX7C93GH6X72FRKVECW7SR5VK'  # Etherscan API key
            
            # USDT contract address on Ethereum
            usdt_contract = '0xdac17f958d2ee523a2206206994597c13d831ec7'
            
            url = f'https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={usdt_contract}&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={api_key}'
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                return False
            
            data = response.json()
            if data.get('status') != '1':
                return False
            
            transactions = data.get('result', [])
            
            # USDT has 6 decimals
            expected_units = float(expected_amount) * 1000000
            tolerance_amount = expected_units * tolerance
            
            for tx in transactions:
                if tx.get('to', '').lower() != address.lower():
                    continue
                
                tx_time = datetime.fromtimestamp(int(tx['timeStamp']), tz=timezone.utc)
                if tx_time < since_time:
                    continue
                
                received_units = int(tx.get('value', 0))
                
                if abs(received_units - expected_units) <= tolerance_amount:
                    tx_hash = tx.get('hash', 'unknown')
                    self.stdout.write(f'   💰 Found: {received_units/1000000} USDT (ERC-20) (TX: {tx_hash[:16]}...)')
                    return True
            
            return False
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   Error checking USDT ERC-20: {str(e)}'))
            return False

    def check_usdt_trc20(self, address, expected_amount, tolerance, since_time):
        """Check USDT TRC-20 (Tron) using TronGrid API"""
        try:
            # USDT contract on Tron
            usdt_contract = 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t'
            
            url = f'https://api.trongrid.io/v1/accounts/{address}/transactions/trc20?limit=50&contract_address={usdt_contract}'
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                return False
            
            data = response.json()
            transactions = data.get('data', [])
            
            expected_units = float(expected_amount) * 1000000
            tolerance_amount = expected_units * tolerance
            
            for tx in transactions:
                if tx.get('to') != address:
                    continue
                
                tx_time = datetime.fromtimestamp(tx['block_timestamp'] / 1000, tz=timezone.utc)
                if tx_time < since_time:
                    continue
                
                received_units = int(tx.get('value', 0))
                
                if abs(received_units - expected_units) <= tolerance_amount:
                    tx_hash = tx.get('transaction_id', 'unknown')
                    self.stdout.write(f'   💰 Found: {received_units/1000000} USDT (TRC-20) (TX: {tx_hash[:16]}...)')
                    return True
            
            return False
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   Error checking USDT TRC-20: {str(e)}'))
            return False

    def check_usdt_bep20(self, address, expected_amount, tolerance, since_time):
        """Check USDT BEP-20 (BSC) using BscScan"""
        try:
            api_key = 'YourApiKeyToken'  # <<< ADD YOUR API KEY HERE
            
            # USDT contract on BSC
            usdt_contract = '0x55d398326f99059ff775485246999027b3197955'
            
            url = f'https://api.bscscan.com/api?module=account&action=tokentx&contractaddress={usdt_contract}&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={api_key}'
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                return False
            
            data = response.json()
            if data.get('status') != '1':
                return False
            
            transactions = data.get('result', [])
            
            expected_units = float(expected_amount) * 1000000000000000000  # 18 decimals on BSC
            tolerance_amount = expected_units * tolerance
            
            for tx in transactions:
                if tx.get('to', '').lower() != address.lower():
                    continue
                
                tx_time = datetime.fromtimestamp(int(tx['timeStamp']), tz=timezone.utc)
                if tx_time < since_time:
                    continue
                
                received_units = int(tx.get('value', 0))
                
                if abs(received_units - expected_units) <= tolerance_amount:
                    tx_hash = tx.get('hash', 'unknown')
                    self.stdout.write(f'   💰 Found: {received_units/1000000000000000000} USDT (BEP-20) (TX: {tx_hash[:16]}...)')
                    return True
            
            return False
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   Error checking USDT BEP-20: {str(e)}'))
            return False

    def check_bnb(self, address, expected_amount, tolerance, since_time):
        """Check BNB (Binance Smart Chain) using BscScan"""
        try:
            self.stdout.write(f'   🔗 Checking BNB blockchain...')
            
            # NOTE: Replace with your BscScan API key (free tier)
            # Get one at: https://bscscan.com/apis
            api_key = 'YourApiKeyToken'  # <<< ADD YOUR API KEY HERE
            
            url = f'https://api.bscscan.com/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={api_key}'
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f'   API Error: {response.status_code}'))
                return False
            
            data = response.json()
            if data.get('status') != '1':
                self.stdout.write(self.style.ERROR(f'   API Error: {data.get("message", "Unknown")}'))
                return False
            
            transactions = data.get('result', [])
            
            # Convert expected amount to wei (BNB has 18 decimals like ETH)
            expected_wei = float(expected_amount) * 1000000000000000000
            tolerance_amount = expected_wei * tolerance
            
            for tx in transactions:
                # Only check incoming transactions
                if tx.get('to', '').lower() != address.lower():
                    continue
                
                # Check transaction time
                tx_time = datetime.fromtimestamp(int(tx['timeStamp']), tz=timezone.utc)
                if tx_time < since_time:
                    continue
                
                # Get received amount in wei
                received_wei = int(tx.get('value', 0))
                
                if abs(received_wei - expected_wei) <= tolerance_amount:
                    tx_hash = tx.get('hash', 'unknown')
                    self.stdout.write(f'   💰 Found: {received_wei/1000000000000000000} BNB (TX: {tx_hash[:16]}...)')
                    return True
            
            return False
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   Error checking BNB: {str(e)}'))
            return False

    def check_litecoin(self, address, expected_amount, tolerance, since_time):
        """Check Litecoin blockchain using BlockCypher API (free, no key needed)"""
        try:
            self.stdout.write(f'   🔗 Checking LTC blockchain...')
            
            # BlockCypher API - free tier: 200 requests/hour, 3 requests/sec
            url = f'https://api.blockcypher.com/v1/ltc/main/addrs/{address}/full?limit=50'
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f'   API Error: {response.status_code}'))
                return False
            
            data = response.json()
            transactions = data.get('txs', [])
            
            # Convert expected amount to litoshis (like satoshis, 1 LTC = 100,000,000 litoshis)
            expected_litoshis = float(expected_amount) * 100000000
            tolerance_amount = expected_litoshis * tolerance
            
            for tx in transactions:
                # Check transaction time
                if 'received' in tx:
                    tx_time = datetime.fromisoformat(tx['received'].replace('Z', '+00:00'))
                    if tx_time < since_time:
                        continue
                
                # Check outputs to our address
                for output in tx.get('outputs', []):
                    if address in output.get('addresses', []):
                        received_litoshis = output.get('value', 0)
                        
                        if abs(received_litoshis - expected_litoshis) <= tolerance_amount:
                            tx_hash = tx.get('hash', 'unknown')
                            self.stdout.write(f'   💰 Found: {received_litoshis/100000000} LTC (TX: {tx_hash[:16]}...)')
                            return True
            
            return False
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   Error checking LTC: {str(e)}'))
            return False

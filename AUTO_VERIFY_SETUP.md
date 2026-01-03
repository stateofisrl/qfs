# 🚀 Automatic Deposit Verification Setup Guide

## ✅ What This Does

Automatically checks blockchain APIs every few minutes to verify deposits and approve them instantly - **no admin intervention needed!**

---

## 📋 Setup Steps

### 1. **Get Free API Keys** (5 minutes)

#### Etherscan (for ETH & USDT ERC-20):
1. Go to https://etherscan.io/register
2. Create free account
3. Go to https://etherscan.io/myapikey
4. Create new API key
5. Copy the key

#### BscScan (for BNB & USDT BEP-20):
1. Go to https://bscscan.com/register
2. Create free account  
3. Go to https://bscscan.com/myapikey
4. Create new API key
5. Copy the key

**Note:** Bitcoin, Litecoin, and USDT TRC-20 (Tron) don't need API keys!

---

### 2. **Add Your API Keys**

Edit `apps/deposits/management/commands/verify_deposits.py`:

Find these lines and replace with your keys:
```python
api_key = 'YourApiKeyToken'  # <<< ADD YOUR API KEY HERE
```

There are 4 places to update:
- Line ~85: Etherscan (for ETH)
- Line ~147: Etherscan (for USDT ERC-20)
- Line ~203: BscScan (for USDT BEP-20)
- Line ~244: BscScan (for BNB)

---

### 3. **Add Your Wallet Addresses**

Go to Django Admin: http://127.0.0.1:8001/admin/

Navigate to **Deposits → Crypto Wallets**

Add your receiving addresses:
- **BTC** - Your Bitcoin address
- **ETH** - Your Ethereum address  
- **USDT** - Can use same address for ERC-20/BEP-20, or separate address for TRC-20
- **BNB** - Your Binance Smart Chain (BSC) address (same as BEP-20)
- **LTC** - Your Litecoin address

Make sure each is marked as **Active** (checkbox enabled)

---

### 4. **Test It Manually**

Run the command once to test:
```bash
python manage.py verify_deposits
```

You should see output like:
```
🔍 Starting automatic deposit verification...
   Tolerance: 1.0%
   Time window: Last 24 hours

Found 3 pending deposit(s)

📋 Checking: user@example.com - 0.0050000 BTC
   🔗 Checking BTC blockchain...
   💰 Found: 0.005 BTC (TX: abc123def456...)
   ✅ APPROVED! Transaction found on blockchain

✨ Verification complete! 1/3 deposits approved
```

---

### 5. **Automate It (Run Every 5 Minutes)**

#### **Windows (Task Scheduler)**:

1. Open **Task Scheduler**
2. Click **Create Basic Task**
3. Name: "Verify Deposits"
4. Trigger: **Daily**, repeat every **5 minutes**
5. Action: **Start a program**
   - Program: `C:\Users\joseph\Downloads\giveaway\.venv\Scripts\python.exe`
   - Arguments: `manage.py verify_deposits`
   - Start in: `C:\Users\joseph\Downloads\giveaway`
6. Finish!

#### **Linux/Mac (Cron Job)**:

Edit crontab:
```bash
crontab -e
```

Add this line:
```bash
*/5 * * * * cd /path/to/giveaway && /path/to/.venv/bin/python manage.py verify_deposits >> /tmp/verify_deposits.log 2>&1
```

---

## ⚙️ Configuration Options

### Check Only Recent Deposits (Last 6 Hours):
```bash
python manage.py verify_deposits --hours 6
```

### Tighter Amount Matching (0.5% Tolerance):
```bash
python manage.py verify_deposits --tolerance 0.005
```

### Combine Options:
```bash
python manage.py verify_deposits --hours 12 --tolerance 0.01
```

---

## 🔍 How It Works

1. **User deposits crypto** → Creates pending deposit in system
2. **Script runs every 5 minutes** → Checks your wallet on blockchain
3. **Finds matching transaction** → Amount matches (within 1% tolerance)
4. **Auto-approves deposit** → User balance updated immediately
5. **Signals trigger** → Referral commissions paid, notifications sent

---

## 📊 What Gets Checked

### Bitcoin (BTC):
- Uses blockchain.info API (free, no key needed)
- Checks last 50 transactions
- Matches amount in satoshis

### Ethereum (ETH):
- Uses Etherscan API
- Checks incoming transactions
- Matches amount in wei

### Binance Coin (BNB):
- Uses BscScan API (Binance Smart Chain)
- Checks incoming BNB transactions
- Matches amount in wei (18 decimals)

### Litecoin (LTC):
- Uses BlockCypher API (free, no key needed)
- Checks last 50 transactions
- Matches amount in litoshis

### USDT:
- **ERC-20** (Ethereum network) - via Etherscan
- **TRC-20** (Tron network) - via TronGrid (no key needed)
- **BEP-20** (BSC network) - via BscScan
- Automatically tries all three chains!

---

## 🛡️ Safety Features

✅ **Amount Tolerance**: Matches deposits within 1% (accounts for network fees)
✅ **Time Window**: Only checks recent deposits (default 24 hours)
✅ **Duplicate Prevention**: Won't approve same deposit twice
✅ **Error Handling**: Continues working even if one API fails
✅ **Audit Trail**: Logs every approval with timestamp

---

## 📝 Logs & Monitoring

Check what happened:
```bash
# View all approved deposits
python manage.py shell
>>> from apps.deposits.models import Deposit
>>> Deposit.objects.filter(status='approved', admin_notes__contains='Auto-verified')
```

---

## ⚠️ Important Notes

1. **API Limits**:
   - Etherscan: 5 calls/second (free tier) - enough for ~300 deposits/minute
   - BscScan: 5 calls/second (for BNB & USDT BEP-20)
   - BlockCypher (LTC): 200 requests/hour, 3 requests/second (free tier)
   - Bitcoin & Tron: No limits

2. **Wallet Addresses**:
   - Use **same address** for all users (system matches by amount)
   - OR use **unique addresses** per user (coming soon)

3. **Network Confirmations**:
   - Script checks immediately (0 confirmations)
   - For safety, consider waiting 1-3 confirmations before crediting large amounts

4. **Tolerance Setting**:
   - Default 1% handles most network fees
   - Tighten to 0.5% for more precision
   - Loosen to 2% if users often send slightly different amounts

---

## 🆘 Troubleshooting

### "API Error: 401"
→ Wrong API key. Double-check you copied it correctly

### "No active wallet found"
→ Go to Admin → Crypto Wallets and add your addresses

### "No matching transaction found"
→ Transaction might not be confirmed yet, or amount doesn't match

### Script not running automatically?
→ Check Task Scheduler (Windows) or crontab (Linux) is configured correctly

---

## 🎉 You're Done!

Deposits will now be automatically verified and approved every 5 minutes!

**Test it:** Have someone send a small test deposit and watch it auto-approve within 5 minutes.

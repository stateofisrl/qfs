# 💰 Supported Cryptocurrencies

Your platform now supports automatic verification for the following cryptocurrencies:

## ✅ Fully Supported (with Auto-Verification)

### 1. Bitcoin (BTC)
- **Blockchain:** Bitcoin
- **API:** blockchain.info (FREE - no key needed)
- **Verification:** ✅ Automatic
- **Address Format:** Legacy or SegWit addresses

### 2. Ethereum (ETH)
- **Blockchain:** Ethereum
- **API:** Etherscan (FREE tier - key required)
- **Verification:** ✅ Automatic
- **Address Format:** 0x... addresses

### 3. Binance Coin (BNB)
- **Blockchain:** Binance Smart Chain (BSC)
- **API:** BscScan (FREE tier - key required)
- **Verification:** ✅ Automatic
- **Address Format:** 0x... addresses (BSC)

### 4. Litecoin (LTC)
- **Blockchain:** Litecoin
- **API:** BlockCypher (FREE - no key needed)
- **Verification:** ✅ Automatic
- **Address Format:** L... or M... addresses
- **Rate Limit:** 200 requests/hour, 3 requests/second

### 5. Tether (USDT)
- **Blockchain:** Multi-chain support
- **Verification:** ✅ Automatic on all chains
- **Supported Networks:**
  - **ERC-20** (Ethereum) - via Etherscan API
  - **TRC-20** (Tron) - via TronGrid API (FREE - no key)
  - **BEP-20** (BSC) - via BscScan API
- **Address Formats:**
  - ERC-20: 0x... (Ethereum)
  - TRC-20: T... (Tron)
  - BEP-20: 0x... (BSC)

---

## 📋 Other Available Options

These are available in the system but need additional API integration:

### 6. USD Coin (USDC)
- Currently available in admin but needs API integration
- Can be added similar to USDT

### 7. Ripple (XRP)
- Available in admin but needs API integration
- Requires XRP Ledger API

### 8. Cardano (ADA)
- Available in admin but needs API integration
- Requires Cardano blockchain API

---

## 🔑 API Keys Needed

To enable full auto-verification:

1. **Etherscan** (for ETH & USDT ERC-20):
   - Get free at: https://etherscan.io/apis
   - Used for: ETH and USDT on Ethereum

2. **BscScan** (for BNB & USDT BEP-20):
   - Get free at: https://bscscan.com/apis
   - Used for: BNB and USDT on BSC

**No API keys needed for:**
- Bitcoin (BTC)
- Litecoin (LTC)
- USDT on Tron (TRC-20)

---

## ⚙️ How to Add Wallets

1. Go to Django Admin: http://127.0.0.1:8001/admin/
2. Navigate to **Deposits → Crypto Wallets**
3. Click **Add Crypto Wallet**
4. Select cryptocurrency and enter your wallet address
5. Check "Is active" to enable
6. Save

---

## 🚀 Auto-Verification Status

| Cryptocurrency | Network | Auto-Verify | API Key Required |
|---------------|---------|-------------|------------------|
| BTC | Bitcoin | ✅ | ❌ |
| ETH | Ethereum | ✅ | ✅ |
| BNB | BSC | ✅ | ✅ |
| LTC | Litecoin | ✅ | ❌ |
| USDT ERC-20 | Ethereum | ✅ | ✅ |
| USDT TRC-20 | Tron | ✅ | ❌ |
| USDT BEP-20 | BSC | ✅ | ✅ |
| USDC | Various | ⏳ | ⏳ |
| XRP | XRP Ledger | ⏳ | ⏳ |
| ADA | Cardano | ⏳ | ⏳ |

**Legend:**
- ✅ = Fully implemented
- ⏳ = Available in system, needs API integration
- ❌ = No key needed
- ✅ = Key required (free tier)

---

## 💡 Tips

1. **Same Address for All:** You can use the same receiving address for all users. The system matches deposits by amount.

2. **Multi-Chain USDT:** USDT can come from 3 different networks. The auto-verification checks all three automatically!

3. **Network Fees:** The 1% tolerance setting accounts for network fees that users might deduct.

4. **Testing:** Always test with small amounts first before adding large wallet balances.

5. **Rate Limits:** Free API tiers have rate limits but are more than sufficient for most platforms:
   - Etherscan: 5 calls/sec = ~300 deposits/minute
   - BscScan: 5 calls/sec = ~300 deposits/minute
   - BlockCypher (LTC): 200 requests/hour = sufficient for most usage

---

## 🔧 Adding More Cryptocurrencies

To add support for more cryptocurrencies:

1. Update `CRYPTO_CHOICES` in [apps/deposits/models.py](apps/deposits/models.py#L14)
2. Add verification method in [verify_deposits.py](apps/deposits/management/commands/verify_deposits.py)
3. Run migrations: `python manage.py makemigrations && python manage.py migrate`
4. Update API keys if needed

---

## 📞 Need Help?

Check the [AUTO_VERIFY_SETUP.md](AUTO_VERIFY_SETUP.md) guide for complete setup instructions!

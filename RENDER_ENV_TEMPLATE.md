# Render Deployment Environment Variables
# Copy and paste these into your Render dashboard
# Settings → Environment → Add variable

# ============================================
# DJANGO CONFIGURATION
# ============================================

# Generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY=change-me-to-generated-secret-key

# NEVER set to True in production
DEBUG=False

# Your Render app URL (will auto-generate domain)
ALLOWED_HOSTS=tesla-investment-platform.onrender.com,www.tesla-investment-platform.onrender.com

# Environment identifier
ENVIRONMENT=production

PYTHON_VERSION=3.12.0

# ============================================
# DATABASE
# ============================================

# Get this from your PostgreSQL service details
# Format: postgresql://user:password@host/database
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@dpg-xxx.internal/investment_platform

# Connection pooling (in seconds)
CONN_MAX_AGE=600

# ============================================
# SECURITY (HTTPS)
# ============================================

CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# CSRF Trusted origins (must include https://)
CSRF_TRUSTED_ORIGINS=https://tesla-investment-platform.onrender.com,https://www.tesla-investment-platform.onrender.com

# ============================================
# EMAIL (Gmail SMTP)
# ============================================

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True

# Your Gmail address
EMAIL_HOST_USER=your-email@gmail.com

# Generate App Password: https://myaccount.google.com/apppasswords
# 16-character password from Gmail (NOT your regular password)
EMAIL_HOST_PASSWORD=xxxx-xxxx-xxxx-xxxx

DEFAULT_FROM_EMAIL=your-email@gmail.com
ADMIN_EMAIL=admin@yourplatform.com

# ============================================
# CACHE & SESSIONS
# ============================================

# In-memory cache for $7 plan (no Redis cost)
# To upgrade: use redis:// URL instead
CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache
CACHE_LOCATION=tesla-investment-cache

# Store sessions in database
SESSION_ENGINE=django.contrib.sessions.backends.db

# ============================================
# CELERY (Background Tasks)
# ============================================

# For $7 plan, you can disable Celery (crypto price updates work without it)
# To enable: add Redis ($7) and uncomment below

# Redis for Celery (optional - add Redis service first)
# CELERY_BROKER_URL=redis://render-redis:6379/0
# CELERY_RESULT_BACKEND=redis://render-redis:6379/1

# Or use database as broker (slower but works on $7)
# CELERY_BROKER_URL=sqla+postgresql://user:pass@host/database
# CELERY_RESULT_BACKEND=db+postgresql://user:pass@host/database

# ============================================
# API KEYS (Optional)
# ============================================

# Crypto prices (CoinGecko - free, no key needed)
# Forex rates (exchangerate-api.com - free tier)
# These are called automatically from apps

# ============================================
# RENDER SPECIFIC
# ============================================

# Auto-deploy on git push
RENDER_AUTO_DEPLOY=true

# PIP cache for faster builds
PIP_CACHE_DIR=/var/cache/pip

# ============================================
# NOTES
# ============================================

# 1. Replace "tesla-investment-platform" with your actual app name
# 2. Replace "YOUR_PASSWORD" with PostgreSQL password from Render
# 3. Get DATABASE_URL from PostgreSQL service → Connection info
# 4. Setup Gmail App Password: https://support.google.com/accounts/answer/185833
# 5. Don't commit this file - store in Render dashboard only
# 6. After deployment, create superuser:
#    - Go to your service → Shell → python manage.py createsuperuser

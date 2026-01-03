# 🚀 RENDER DEPLOYMENT GUIDE - $7 Standard Plan
**Tesla Investment Platform**  
**Cost:** $7/month web + $7/month database = $14/month total

---

## 📋 SETUP CHECKLIST

### Step 1: Prepare Repository
```bash
# Make build.sh executable
chmod +x build.sh

# Commit changes
git add -A
git commit -m "Optimize for Render $7 Standard deployment"
git push origin main
```

### Step 2: Create Render Account
1. Go to https://render.com
2. Sign up (use GitHub for easy deploy)
3. Create new project

### Step 3: Create PostgreSQL Database
1. Click **"New +"** → **"PostgreSQL"**
2. **Name:** `tesla-investment-db`
3. **Region:** Oregon (or your preferred)
4. **Database Name:** `investment_platform`
5. **User:** `postgres`
6. **Plan:** Standard ($7/month)
7. Click **"Create Database"**
8. **Copy the Internal Database URL** (you'll need this)

### Step 4: Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Fill in:
   - **Name:** `tesla-investment-platform`
   - **Region:** Oregon
   - **Branch:** main
   - **Runtime:** Python 3
   - **Build Command:** `chmod +x build.sh && ./build.sh`
   - **Start Command:** `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --worker-class sync --timeout 60 --access-logfile - --error-logfile -`
   - **Plan:** Standard ($7/month)

### Step 5: Add Environment Variables
In the Render dashboard, go to your web service → **Environment** and add:

```env
# Django
PYTHON_VERSION=3.12.0
DEBUG=False
ENVIRONMENT=production
ALLOWED_HOSTS=your-app-name.onrender.com,www.your-app-name.onrender.com

# Database (get this from PostgreSQL service)
DATABASE_URL=postgresql://postgres:password@dpg-xxx.internal/investment_platform
CONN_MAX_AGE=600

# Security
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com,https://www.your-app-name.onrender.com

# Email (Gmail SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
ADMIN_EMAIL=admin@example.com

# Caching
CACHE_LOCATION=:memory:
SESSION_ENGINE=django.contrib.sessions.backends.db

# Generate SECRET_KEY with:
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY=your-generated-secret-key-here
```

### Step 6: Configure Email (Gmail)
1. Enable 2FA on your Gmail account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use the 16-character password in `EMAIL_HOST_PASSWORD`

### Step 7: Deploy!
1. Click **"Create Web Service"**
2. Render will auto-deploy from your main branch
3. **Wait 2-5 minutes** for build to complete
4. View logs in the dashboard

### Step 8: Create Superuser
Once deployment succeeds:
1. Go to your web service dashboard
2. Click **"Shell"** (opens terminal)
3. Run:
```bash
python manage.py createsuperuser
```

### Step 9: Verify Deployment
- **Frontend:** https://your-app-name.onrender.com
- **Admin:** https://your-app-name.onrender.com/admin
- **API:** https://your-app-name.onrender.com/api/users/me/

---

## 🔧 OPTIMIZATION FOR $7 PLAN

### Memory Management
- **Workers:** 2 (optimized for $7 plan memory)
- **Worker Class:** sync (best for memory constraints)
- **Timeout:** 60 seconds per request

### Database
- **Connection Pooling:** 600 seconds max age
- **Health Checks:** Enabled
- **Statement Timeout:** 30 seconds

### Build
- **No Cache Pip:** Faster builds (--no-cache-dir)
- **Clear Static:** Remove old static files before upload
- **Minimal Dependencies:** requirements.txt is lean

### Performance
- **WhiteNoise:** Efficient static file serving
- **Django Admin Checks:** Optimized
- **QuerySet Optimization:** Already implemented

---

## 📊 RESOURCE ALLOCATION

### Web Service ($7/month)
- **CPU:** 0.5 (shared)
- **Memory:** 512 MB
- **Bandwidth:** 100 GB/month
- **Auto-restart:** Enabled

### Database ($7/month)
- **CPU:** Shared
- **RAM:** 256 MB
- **Storage:** 10 GB
- **Connections:** Up to 20

**Total Cost:** $14/month (great for MVP!)

---

## 🔄 AUTO-DEPLOY & UPDATES

Render will **automatically redeploy** when you push to `main`:
```bash
# Make changes
git add -A
git commit -m "Your changes"
git push origin main

# Render detects push and auto-deploys
# Check dashboard for build progress
```

---

## 🐛 TROUBLESHOOTING

### Build Fails
```bash
# Check build logs in Render dashboard
# Common issues:
# 1. Missing environment variables → Add in dashboard
# 2. Database not connected → Check DATABASE_URL
# 3. Static files error → Verify STATIC_ROOT

# Rebuild manually:
# Dashboard → Logs → "Manual Deploy"
```

### "Application Error 500"
1. Check Logs in Render dashboard
2. Verify all env variables are set
3. Check database connection: `echo $DATABASE_URL`
4. Verify migrations ran: `python manage.py showmigrations`

### Database Connection Timeout
1. Ensure PostgreSQL is running
2. Check Internal Database URL format
3. Verify CONN_MAX_AGE is set
4. Check firewall (should allow internal Render traffic)

### Static Files 404
```bash
# Force static files collection
python manage.py collectstatic --noinput --clear
git add staticfiles/
git commit -m "Collect static files"
git push
```

### Email Not Sending
1. Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
2. Check Gmail app password (not account password!)
3. Ensure 2FA is enabled on Gmail
4. Check ADMIN_EMAIL is set

---

## 🚨 BEFORE GOING LIVE

- [ ] SECRET_KEY is strong (50+ characters)
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS set correctly
- [ ] Email credentials working
- [ ] Database migrations complete
- [ ] Superuser created
- [ ] Test login at /admin/
- [ ] Test deposit form
- [ ] Test API endpoints
- [ ] Monitor logs for errors

---

## 📈 MONITORING & SCALING

### Monitor Usage
- **Render Dashboard:** CPU, Memory, Bandwidth
- **Logs:** View in real-time
- **Alerts:** Set up email alerts for errors

### Scale Up (if needed)
- Upgrade web service to **Standard** ($7) → **Pro** ($12)
- Upgrade database to **Standard+** ($15) → **Pro** ($29)
- Add **Redis** for caching ($7)
- Add **Celery Worker** for background jobs ($7)

### Costs Breakdown
| Component | $7 | $12 | $15+ |
|-----------|-----|-----|------|
| Web Service | Standard | Pro | Pro+ |
| Database | Starter | Standard | Standard+ |
| **Total** | **$14** | **$19** | **$22+** |

---

## 🔐 SECURITY

### HTTPS
✅ **Automatic** - Render provides free SSL certificate

### Environment Variables
✅ **Encrypted** - Stored securely in Render
✅ **Never committed** to git

### Database
✅ **Internal network** - Not exposed to internet
✅ **PostgreSQL** - Industry standard

### Backups
⚠️ **Manual backups recommended** (Render provides automatic daily backups for Pro+ plans)

---

## 🎯 NEXT STEPS

1. **Deploy:** Follow Steps 1-9 above
2. **Configure:** Set up email and API keys
3. **Test:** Verify all features work
4. **Monitor:** Watch logs for errors
5. **Optimize:** Adjust workers/memory as needed
6. **Scale:** Add services as traffic grows

---

## 📞 SUPPORT

- **Render Docs:** https://render.com/docs
- **Django Docs:** https://docs.djangoproject.com
- **GitHub Issues:** Check deployment guides

**Good luck! 🚀**

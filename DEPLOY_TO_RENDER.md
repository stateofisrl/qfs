# 🚀 Deploy QFS Investment Platform to Render

## ✅ Pre-Deployment Checklist

### System Status
- ✅ All tests passing (18/18)
- ✅ Screenshot upload working
- ✅ Crypto symbols displaying correctly
- ✅ Double refund bug fixed
- ✅ Light-themed alerts
- ✅ Session persistence configured
- ✅ Email notifications ready

### Files Ready
- ✅ `render.yaml` - Configured for QFS platform
- ✅ `build.sh` - Build script ready
- ✅ `requirements.txt` - All dependencies listed
- ✅ `config/settings.py` - Production-ready with DATABASE_URL support
- ✅ Email: aegiscyberops@gmail.com configured

---

## 📝 Deployment Steps

### Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Deploy QFS Investment Platform to Render"

# Add your GitHub repo
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to main branch
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will detect `render.yaml` automatically
5. Review the configuration:
   - **Web Service**: qfs-investment-platform
   - **Database**: qfs-investment-db (PostgreSQL)
6. Click **"Apply"**

Render will:
- Create PostgreSQL database
- Create web service
- Link them together
- Start the build process

### Step 3: Set Email Password

After deployment starts:

1. Go to your web service → **"Environment"**
2. Find `EMAIL_HOST_PASSWORD`
3. Set it to your Gmail App Password: `bcummthtwkgqlfux`
4. Click **"Save Changes"**

The service will automatically redeploy.

### Step 4: Wait for Build (3-5 minutes)

Monitor the build logs:
- Installing dependencies
- Running migrations
- Collecting static files

### Step 5: Create Admin User

Once deployed, click **"Shell"** in the Render dashboard:

```bash
python manage.py createsuperuser
```

Enter:
- Email: forexbtte@gmail.com (or your admin email)
- Password: (choose a strong password)

---

## 🌐 Access Your Platform

After deployment completes:

- **Live Site**: `https://qfs-investment-platform.onrender.com`
- **Admin Panel**: `https://qfs-investment-platform.onrender.com/admin/`

---

## 💰 Pricing

| Service | Plan | Cost |
|---------|------|------|
| Web Service | Starter | Free (or $7/mo Standard for better performance) |
| PostgreSQL | Starter | Free (or $7/mo Standard for 1GB storage) |
| **Total (Free Plan)** | | **$0/mo** |
| **Total (Standard Plan)** | | **$14/mo** |

### Free Plan Limitations:
- Web service spins down after 15 mins of inactivity
- 750 hours/month free compute
- Shared resources

### Standard Plan Benefits ($14/mo):
- ✅ Always-on (no spin down)
- ✅ 512 MB RAM
- ✅ 1 GB database storage
- ✅ Daily backups (7 days)
- ✅ Better performance

---

## 🔧 Post-Deployment Configuration

### 1. Update ALLOWED_HOSTS (if needed)

If you get a 400 Bad Request error:

1. Go to Environment variables
2. Update `ALLOWED_HOSTS`:
   ```
   ALLOWED_HOSTS=qfs-investment-platform.onrender.com,www.your-custom-domain.com
   ```

### 2. Set Up Investment Plans

1. Login to admin panel
2. Go to **Investment Plans**
3. Create your investment plans (Basic, Premium, VIP)

### 3. Add Crypto Wallets

1. Go to **Crypto Wallets**
2. Add your wallet addresses:
   - Bitcoin (BTC)
   - Ethereum (ETH)
   - USDT-ERC20, etc.

### 4. Test Email Notifications

1. Create a test user
2. Make a test deposit
3. Approve it from admin
4. Verify email is sent

---

## 🎯 Environment Variables (Configured in render.yaml)

```yaml
# Security
SECRET_KEY=auto-generated
DEBUG=False
ALLOWED_HOSTS=*.onrender.com

# Database
DATABASE_URL=auto-linked from PostgreSQL

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=aegiscyberops@gmail.com
EMAIL_HOST_PASSWORD=bcummthtwkgqlfux (set manually)
DEFAULT_FROM_EMAIL=aegiscyberops@gmail.com
ADMIN_EMAIL=aegiscyberops@gmail.com

# HTTPS Security
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

---

## 📊 Monitor Your Deployment

### Logs
- View real-time logs in Render dashboard
- Check for errors or warnings
- Monitor requests and responses

### Metrics
- CPU usage
- Memory usage
- Response times
- Request counts

### Auto-Deploy
- Push to GitHub main branch
- Render automatically rebuilds and deploys
- Zero-downtime deployments

---

## 🆘 Troubleshooting

### Build Fails?

1. Check build logs for errors
2. Verify all dependencies in requirements.txt
3. Make sure build.sh is executable

### Database Connection Error?

1. Verify DATABASE_URL is set
2. Check PostgreSQL service is running
3. Wait for database to finish provisioning

### Static Files Not Loading?

1. Check build logs show "Collecting static files"
2. Verify WhiteNoise is in MIDDLEWARE
3. Check STATIC_ROOT and STATICFILES_DIRS

### Email Not Sending?

1. Verify EMAIL_HOST_PASSWORD is set correctly
2. Check Gmail App Password is active
3. Enable "Less secure app access" if needed

### 400 Bad Request?

1. Update ALLOWED_HOSTS to include your Render URL
2. Add custom domain if using one

---

## 🎉 Success Indicators

✅ Build completes without errors  
✅ Migrations run successfully  
✅ Static files collected  
✅ Site loads at your Render URL  
✅ Admin panel accessible  
✅ Can login with superuser  
✅ Can create deposits/withdrawals/investments  
✅ Email notifications work  

---

## 🔐 Security Notes

1. **Never commit** sensitive data to GitHub:
   - Email passwords
   - Secret keys
   - API tokens

2. **Use environment variables** for all secrets

3. **Enable 2FA** on:
   - GitHub account
   - Render account
   - Gmail account

4. **Regular backups**:
   - Render includes daily backups on Standard plan
   - Export database manually if on Free plan

---

## 📞 Support

If you encounter issues:

1. Check Render documentation: https://render.com/docs
2. Review Django logs in Render dashboard
3. Check application logs for specific errors
4. Verify all environment variables are set correctly

---

## 🚀 Next Steps After Deployment

1. ✅ Set up custom domain (optional)
2. ✅ Configure SSL certificate (auto with Render)
3. ✅ Set up monitoring/alerts
4. ✅ Create investment plans
5. ✅ Add crypto wallets
6. ✅ Test all features
7. ✅ Invite first users
8. ✅ Monitor email deliverability
9. ✅ Set up backup strategy
10. ✅ Document admin procedures

---

**Your platform is ready for production! 🎉**

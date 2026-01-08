# Email Setup for Render Deployment

## ⚠️ CRITICAL: Set Email Password

**Email verification will NOT work until you complete these steps:**

---

## Step 1: Add EMAIL_HOST_PASSWORD to Render

1. Go to https://dashboard.render.com
2. Click on **qfs-investment-platform** (your web service)
3. Click **"Environment"** tab on the left
4. Click **"Add Environment Variable"**
5. Add:
   - **Key**: `EMAIL_HOST_PASSWORD`
   - **Value**: `bcummthtwkgqlfux`
6. Click **"Save Changes"**
7. Render will automatically redeploy (wait 2-3 minutes)

---

## Step 2: Verify Gmail App Password

If emails still don't send, the app password might be invalid:

### Generate New Gmail App Password:

1. Go to https://myaccount.google.com/apppasswords
2. Sign in with **aegiscyberops@gmail.com**
3. Click **"Create"** or **"Generate app password"**
4. Select:
   - **App**: Mail
   - **Device**: Other (Custom name) → "QFS Platform"
5. Click **"Generate"**
6. Copy the **16-character password** (no spaces)
7. Update `EMAIL_HOST_PASSWORD` in Render with new password
8. Save and wait for redeploy

---

## Step 3: Test Email Sending

After setting the password:

1. Go to your site: https://qfs-investment-platform.onrender.com
2. Register a new user
3. Check if verification email arrives
4. If not, check Render Logs for errors

---

## Troubleshooting

### Check Render Logs for Email Errors:

1. Dashboard → **Logs** tab
2. Search for:
   - `SMTPAuthenticationError`
   - `Connection refused`
   - `Email`
3. Common errors:

#### Error: SMTPAuthenticationError
**Fix**: App password is wrong. Generate new one.

#### Error: Connection refused
**Fix**: Gmail might be blocking. Try:
- Verify 2-Step Verification is ON
- Generate fresh app password
- Check if aegiscyberops@gmail.com is accessible

#### Error: No error but no email
**Fix**: Check spam folder or Gmail might be silently blocking

---

## Alternative: Use SendGrid (If Gmail Fails)

If Gmail continues to fail, switch to SendGrid (free 100 emails/day):

1. Sign up at https://sendgrid.com
2. Get API key
3. Update Render environment variables:
   ```
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.sendgrid.net
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=apikey
   EMAIL_HOST_PASSWORD=<your-sendgrid-api-key>
   DEFAULT_FROM_EMAIL=aegiscyberops@gmail.com
   ```

---

## Verify Email is Working

### Test in Render Shell:

1. Click **"Shell"** in Render dashboard
2. Run:
   ```python
   python manage.py shell
   ```
3. In the shell:
   ```python
   from django.core.mail import send_mail
   from django.conf import settings
   
   send_mail(
       'Test Email',
       'Testing email from QFS Platform',
       settings.DEFAULT_FROM_EMAIL,
       ['your-email@gmail.com'],  # Replace with your email
       fail_silently=False,
   )
   ```
4. Check if email arrives
5. If error shows, share it for debugging

---

## Current Email Configuration

- **Email Backend**: SMTP
- **Host**: smtp.gmail.com
- **Port**: 587
- **TLS**: Enabled
- **From Email**: aegiscyberops@gmail.com
- **Password**: Must be set in Render environment

---

## ✅ Checklist

- [ ] EMAIL_HOST_PASSWORD added to Render
- [ ] Render redeployed after adding password
- [ ] Gmail 2-Step Verification is ON
- [ ] App password is valid (16 characters, no spaces)
- [ ] Test email sent successfully
- [ ] Registration verification email received
- [ ] Investment notification emails working

---

**After completing Step 1, emails should work within 2-3 minutes (after redeploy).**

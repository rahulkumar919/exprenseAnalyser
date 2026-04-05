# 🚀 Quick Start - OTP Email Verification

## What's New?
Your expense tracker now has email OTP verification! Users must verify their email before accessing the app.

---

## Setup in 3 Steps

### Step 1: Install Flask-Mail
```bash
pip install flask-mail
```

### Step 2: Configure Gmail (Easiest Method)

1. **Get Gmail App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Create app password for "Mail"
   - Copy the 16-character password

2. **Set Environment Variables (Windows PowerShell):**
```powershell
$env:MAIL_USERNAME="your-email@gmail.com"
$env:MAIL_PASSWORD="your-16-char-app-password"
```

**Or for Windows CMD:**
```cmd
set MAIL_USERNAME=your-email@gmail.com
set MAIL_PASSWORD=your-16-char-app-password
```

### Step 3: Run the App
```bash
python app.py
```

---

## How to Test

1. **Go to:** http://localhost:5000/login
2. **Click "Sign Up"**
3. **Fill in:**
   - Username: testuser
   - Email: your-email@gmail.com
   - Password: test123
4. **Click "Sign Up"**
5. **Check your email** for the OTP code
6. **Enter the 6-digit OTP**
7. **Click "Verify OTP"**
8. **Login with your credentials**

---

## Features

✅ Beautiful OTP email with gradient design
✅ 6-digit OTP code
✅ 10-minute expiration
✅ Auto-focus OTP inputs
✅ Paste support
✅ Resend OTP option
✅ Countdown timer
✅ Secure verification

---

## Troubleshooting

**Email not sending?**
- Check your Gmail App Password
- Make sure 2-Step Verification is enabled
- Check spam folder

**OTP expired?**
- Click "Resend OTP" to get a new code

**Can't login?**
- Make sure you verified your email first
- Check username and password

---

## Default Configuration

If you don't set environment variables, the app uses:
- MAIL_SERVER: smtp.gmail.com
- MAIL_PORT: 587
- MAIL_USERNAME: your-email@gmail.com (you must change this!)
- MAIL_PASSWORD: your-app-password (you must change this!)

---

## Production Tips

For production, use:
- SendGrid (100 emails/day free)
- AWS SES ($0.10 per 1000 emails)
- Mailgun (5000 emails/month free)

See EMAIL_SETUP.md for detailed production setup.

---

**That's it! Your OTP system is ready! 🎉**

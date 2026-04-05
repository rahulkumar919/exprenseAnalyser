# 📧 Email OTP Setup Guide

## Overview
Your Expense Analyser now has email OTP verification for user registration!

## Features Implemented
✅ Email OTP verification on signup
✅ 6-digit OTP code generation
✅ Beautiful HTML email template
✅ 10-minute OTP expiration
✅ Resend OTP functionality
✅ Auto-focus OTP input fields
✅ Paste support for OTP
✅ Countdown timer
✅ User data stored only after verification

---

## Setup Instructions

### Step 1: Install Flask-Mail
```bash
pip install flask-mail
```

### Step 2: Configure Email Settings

#### Option A: Using Gmail (Recommended for Testing)

1. **Enable 2-Step Verification**
   - Go to https://myaccount.google.com/security
   - Enable "2-Step Verification"

2. **Generate App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select app: "Mail"
   - Select device: "Other (Custom name)"
   - Enter: "Expense Analyser"
   - Copy the 16-character password

3. **Set Environment Variables**

**Windows (PowerShell):**
```powershell
$env:MAIL_SERVER="smtp.gmail.com"
$env:MAIL_PORT="587"
$env:MAIL_USERNAME="your-email@gmail.com"
$env:MAIL_PASSWORD="your-16-char-app-password"
```

**Windows (CMD):**
```cmd
set MAIL_SERVER=smtp.gmail.com
set MAIL_PORT=587
set MAIL_USERNAME=your-email@gmail.com
set MAIL_PASSWORD=your-16-char-app-password
```

**Linux/Mac:**
```bash
export MAIL_SERVER="smtp.gmail.com"
export MAIL_PORT="587"
export MAIL_USERNAME="your-email@gmail.com"
export MAIL_PASSWORD="your-16-char-app-password"
```

#### Option B: Using .env File (Recommended for Production)

1. Create `.env` file in project root:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

2. Install python-dotenv:
```bash
pip install python-dotenv
```

3. Update `app.py` to load .env:
```python
from dotenv import load_dotenv
load_dotenv()  # Add this at the top
```

---

## How It Works

### Registration Flow

1. **User fills signup form** (username, email, password)
2. **Backend generates 6-digit OTP**
3. **OTP sent to user's email** (beautiful HTML template)
4. **User data stored in session** (not in database yet)
5. **User enters OTP** (6 input fields with auto-focus)
6. **Backend verifies OTP** (checks validity and expiration)
7. **User account created** in database
8. **User redirected to login page**

### Database Schema

New table: `otp_verification`
```sql
CREATE TABLE otp_verification (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    otp TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_used INTEGER DEFAULT 0
)
```

Updated `users` table:
```sql
ALTER TABLE users ADD COLUMN is_verified INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
```

---

## API Endpoints

### 1. Signup (Send OTP)
```
POST /signup
Body: { "username": "john", "email": "john@example.com", "password": "pass123" }
Response: { "message": "OTP sent to your email", "email": "john@example.com" }
```

### 2. Verify OTP
```
POST /verify-otp
Body: { "email": "john@example.com", "otp": "123456" }
Response: { "message": "Email verified successfully!", "user_id": 1 }
```

### 3. Resend OTP
```
POST /resend-otp
Body: { "email": "john@example.com" }
Response: { "message": "New OTP sent to your email" }
```

### 4. Login (Requires Verification)
```
POST /login
Body: { "username": "john", "password": "pass123" }
Response: { "message": "Login successful", "user_id": 1, "username": "john" }
```

---

## Testing

### 1. Start the Server
```bash
python app.py
```

### 2. Test Registration
1. Go to http://localhost:5000/login
2. Click "Sign Up" tab
3. Fill in username, email, password
4. Click "Sign Up"
5. Check your email for OTP
6. Enter the 6-digit OTP
7. Click "Verify OTP"
8. You'll be redirected to login

### 3. Test Login
1. Enter your username and password
2. Click "Login"
3. You'll be redirected to dashboard

---

## Email Template Preview

The OTP email includes:
- Professional header with gradient
- Large, easy-to-read OTP code
- Expiration time (10 minutes)
- Security tips
- Branded footer

---

## Troubleshooting

### Issue: "Failed to send OTP"
**Solution**: Check your email credentials and internet connection

### Issue: "Invalid OTP"
**Solution**: Make sure you entered the correct 6-digit code

### Issue: "OTP has expired"
**Solution**: Click "Resend OTP" to get a new code

### Issue: "Please verify your email first"
**Solution**: Complete the OTP verification process before logging in

### Issue: Gmail not sending emails
**Solution**: 
- Make sure 2-Step Verification is enabled
- Use App Password, not your regular password
- Check if "Less secure app access" is enabled (if not using App Password)

---

## Production Recommendations

### 1. Use SendGrid or AWS SES
Gmail has sending limits. For production, use:
- **SendGrid**: 100 emails/day free
- **AWS SES**: $0.10 per 1000 emails
- **Mailgun**: 5000 emails/month free

### 2. Add Rate Limiting
Prevent OTP spam:
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@auth_bp.route('/signup', methods=['POST'])
@limiter.limit("3 per hour")
def signup():
    # ...
```

### 3. Store Secrets Securely
- Use environment variables
- Never commit `.env` to git
- Use AWS Secrets Manager or similar in production

### 4. Add Email Queue
For better performance:
```python
from celery import Celery

@celery.task
def send_otp_email_async(email, otp):
    send_otp_email(email, otp)
```

---

## Security Features

✅ OTP expires after 10 minutes
✅ OTP can only be used once
✅ Passwords are hashed (werkzeug)
✅ Session-based temporary storage
✅ Email validation
✅ Rate limiting ready

---

## Next Steps

1. Set up your email credentials
2. Test the registration flow
3. Customize the email template (in `routes/auth.py`)
4. Add rate limiting
5. Consider using SendGrid for production

---

**Need Help?**
Check the console logs for detailed error messages!

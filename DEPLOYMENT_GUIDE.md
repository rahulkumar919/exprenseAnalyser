# ExpenseSense Pro - Production Deployment Guide

## 🚀 Overview

This guide covers deploying your upgraded ExpenseSense Pro application to production using modern cloud platforms.

---

## 📋 Pre-Deployment Checklist

### Backend
- [ ] All environment variables configured
- [ ] Database migrations tested
- [ ] Rate limiting configured
- [ ] CORS origins set correctly
- [ ] Logging configured
- [ ] Error handling tested
- [ ] Security headers added

### Frontend
- [ ] API URL configured
- [ ] Build tested locally
- [ ] Environment variables set
- [ ] Error boundaries added
- [ ] Loading states implemented
- [ ] SEO meta tags added

---

## 🗄️ Database Setup (PostgreSQL)

### Option 1: Render PostgreSQL

1. **Create Database**:
   - Go to Render Dashboard
   - Click "New +" → "PostgreSQL"
   - Choose plan (Free tier available)
   - Note the connection string

2. **Connection String Format**:
```
postgresql://user:password@host:5432/database
```

### Option 2: Railway PostgreSQL

1. **Create Database**:
   - Go to Railway Dashboard
   - Click "New Project"
   - Add "PostgreSQL" service
   - Copy connection string from variables

### Option 3: Supabase

1. **Create Project**:
   - Go to Supabase Dashboard
   - Create new project
   - Get connection string from Settings → Database

---

## 🔧 Backend Deployment

### Option 1: Render

#### Step 1: Prepare Repository

Create `render.yaml`:
```yaml
services:
  - type: web
    name: expensesense-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn run:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: expensesense-db
          property: connectionString
      - key: CORS_ORIGINS
        value: https://your-frontend.vercel.app

databases:
  - name: expensesense-db
    databaseName: expensesense
    user: expensesense
```

#### Step 2: Deploy

```bash
# Add gunicorn to requirements.txt
echo "gunicorn==21.2.0" >> requirements.txt

# Commit changes
git add .
git commit -m "Prepare for deployment"
git push origin main

# Deploy on Render
# 1. Connect GitHub repository
# 2. Select branch
# 3. Render will auto-deploy
```

#### Step 3: Run Migrations

```bash
# In Render Shell
flask db upgrade
```

---

### Option 2: Railway

#### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
railway login
```

#### Step 2: Deploy

```bash
cd backend

# Initialize Railway project
railway init

# Add PostgreSQL
railway add

# Set environment variables
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=your-secret-key
railway variables set JWT_SECRET_KEY=your-jwt-secret
railway variables set CORS_ORIGINS=https://your-frontend.vercel.app

# Deploy
railway up
```

#### Step 3: Run Migrations

```bash
railway run flask db upgrade
```

---

### Option 3: Heroku

#### Step 1: Prepare Files

Create `Procfile`:
```
web: gunicorn run:app
release: flask db upgrade
```

Create `runtime.txt`:
```
python-3.11.0
```

#### Step 2: Deploy

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create expensesense-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key
heroku config:set JWT_SECRET_KEY=your-jwt-secret
heroku config:set CORS_ORIGINS=https://your-frontend.vercel.app

# Deploy
git push heroku main

# Run migrations (automatic with release command)
```

---

## 🎨 Frontend Deployment

### Option 1: Vercel (Recommended)

#### Step 1: Prepare Project

Create `vercel.json`:
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

#### Step 2: Deploy

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Set environment variables in Vercel Dashboard
# VITE_API_URL=https://your-backend.render.com/api

# Deploy to production
vercel --prod
```

---

### Option 2: Netlify

#### Step 1: Prepare Project

Create `netlify.toml`:
```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  NODE_VERSION = "18"
```

#### Step 2: Deploy

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Initialize
cd frontend
netlify init

# Set environment variables
netlify env:set VITE_API_URL https://your-backend.render.com/api

# Deploy
netlify deploy --prod
```

---

### Option 3: Cloudflare Pages

#### Step 1: Deploy

```bash
# Install Wrangler CLI
npm install -g wrangler

# Login
wrangler login

# Deploy
cd frontend
npx wrangler pages publish dist --project-name=expensesense
```

#### Step 2: Set Environment Variables

In Cloudflare Dashboard:
- Go to Pages → Your Project → Settings → Environment Variables
- Add: `VITE_API_URL=https://your-backend.render.com/api`

---

## 🔒 Security Configuration

### Backend Security Headers

Add to `app/__init__.py`:
```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

### Environment Variables (Production)

**Backend (.env)**:
```bash
FLASK_ENV=production
DEBUG=False
SECRET_KEY=<generate-with-secrets.token_urlsafe(32)>
JWT_SECRET_KEY=<generate-with-secrets.token_urlsafe(32)>
DATABASE_URL=postgresql://user:pass@host:5432/db
CORS_ORIGINS=https://your-frontend.vercel.app
RATE_LIMIT_ENABLED=True
LOG_LEVEL=INFO
```

**Frontend (.env)**:
```bash
VITE_API_URL=https://your-backend.render.com/api
VITE_APP_NAME=ExpenseSense Pro
```

---

## 📊 Monitoring & Logging

### Backend Logging

Logs are stored in `logs/app.log`. To view:

**Render**:
```bash
# View logs in Render Dashboard
# Or use CLI
render logs -s your-service-name
```

**Railway**:
```bash
railway logs
```

### Frontend Error Tracking

Add Sentry (optional):

```bash
npm install @sentry/react
```

```javascript
// src/main.jsx
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "your-sentry-dsn",
  environment: import.meta.env.MODE,
});
```

---

## 🔄 CI/CD Setup

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Render
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Vercel
        run: |
          npm install -g vercel
          cd frontend
          vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

---

## 🧪 Testing Production

### Backend Health Check

```bash
curl https://your-backend.render.com/api/auth/me
# Should return 401 (unauthorized) - means API is working
```

### Frontend Check

```bash
curl https://your-frontend.vercel.app
# Should return HTML
```

### Full Flow Test

1. Register new user
2. Login
3. Create expense
4. View analytics
5. Export CSV

---

## 📈 Performance Optimization

### Backend

1. **Enable Gzip Compression**:
```python
from flask_compress import Compress
Compress(app)
```

2. **Database Connection Pooling**:
```python
# In config.py
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}
```

3. **Caching** (Optional):
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

### Frontend

1. **Code Splitting**:
```javascript
// Use React.lazy
const Dashboard = lazy(() => import('./pages/Dashboard'));
```

2. **Image Optimization**:
```javascript
// Use WebP format
// Lazy load images
```

3. **Bundle Analysis**:
```bash
npm run build -- --analyze
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. CORS Errors
```python
# Ensure CORS_ORIGINS includes your frontend URL
CORS_ORIGINS=https://your-frontend.vercel.app,https://www.your-frontend.vercel.app
```

#### 2. Database Connection
```bash
# Test connection
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); print(db.engine.url)"
```

#### 3. JWT Token Issues
```javascript
// Check token expiration
// Ensure refresh token logic works
```

#### 4. Build Failures
```bash
# Clear cache
npm clean-install
rm -rf node_modules package-lock.json
npm install
```

---

## 📱 Custom Domain Setup

### Backend (Render)

1. Go to Settings → Custom Domain
2. Add your domain: `api.yourdomain.com`
3. Update DNS records as instructed

### Frontend (Vercel)

1. Go to Settings → Domains
2. Add your domain: `yourdomain.com`
3. Update DNS records as instructed

---

## 🔐 SSL/HTTPS

Both Render and Vercel provide automatic SSL certificates. No additional configuration needed.

---

## 💾 Backup Strategy

### Database Backups

**Render**:
- Automatic daily backups on paid plans
- Manual backup: Export from dashboard

**Railway**:
- Automatic backups
- Manual: `railway run pg_dump > backup.sql`

### Code Backups

- Use Git (already done)
- Tag releases: `git tag v2.0.0`

---

## 📊 Cost Estimation

### Free Tier (Development)

- **Backend**: Render Free (750 hours/month)
- **Database**: Render PostgreSQL Free (90 days)
- **Frontend**: Vercel Free (unlimited)
- **Total**: $0/month

### Production (Small Scale)

- **Backend**: Render Starter ($7/month)
- **Database**: Render PostgreSQL Starter ($7/month)
- **Frontend**: Vercel Pro ($20/month)
- **Total**: ~$34/month

### Production (Medium Scale)

- **Backend**: Railway Pro ($20/month)
- **Database**: Supabase Pro ($25/month)
- **Frontend**: Vercel Pro ($20/month)
- **Total**: ~$65/month

---

## ✅ Post-Deployment Checklist

- [ ] Backend API accessible
- [ ] Frontend loads correctly
- [ ] User registration works
- [ ] Login/logout works
- [ ] Expenses CRUD works
- [ ] Analytics display correctly
- [ ] CSV export works
- [ ] Mobile responsive
- [ ] SSL certificate active
- [ ] Error tracking configured
- [ ] Monitoring setup
- [ ] Backups configured

---

## 📞 Support Resources

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Railway Docs**: https://docs.railway.app
- **Flask Docs**: https://flask.palletsprojects.com
- **React Docs**: https://react.dev

---

**Last Updated**: April 2026  
**Version**: 2.0.0

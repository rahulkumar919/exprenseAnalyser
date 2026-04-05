# ExpenseSense Pro v2.0 - Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will get your upgraded ExpenseSense Pro running locally.

---

## Prerequisites

- Python 3.9+ installed
- Node.js 18+ installed
- Git installed
- Code editor (VS Code recommended)

---

## Step 1: Clone & Setup (2 minutes)

```bash
# Navigate to project
cd "project 2"

# You should see two folders: backend/ and frontend/
```

---

## Step 2: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Start backend server
python run.py
```

Backend will run on: `http://localhost:5000`

---

## Step 3: Frontend Setup (1 minute)

Open a NEW terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Start frontend server
npm run dev
```

Frontend will run on: `http://localhost:3000`

---

## Step 4: Test the Application

1. Open browser: `http://localhost:3000`
2. Click "Sign Up"
3. Create account:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `Test1234`
4. Login with credentials
5. Add your first expense!

---

## 🎯 Quick Commands Reference

### Backend Commands

```bash
# Start server
python run.py

# Run migrations
flask db migrate -m "message"
flask db upgrade

# Create admin user (optional)
flask shell
>>> from app.models import User
>>> user = User(username='admin', email='admin@example.com')
>>> user.set_password('Admin1234')
>>> db.session.add(user)
>>> db.session.commit()
```

### Frontend Commands

```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

---

## 🔧 Configuration

### Backend (.env)

```bash
FLASK_ENV=development
SECRET_KEY=dev-secret-key
JWT_SECRET_KEY=jwt-secret-key
DATABASE_URL=sqlite:///expenses.db
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env)

```bash
VITE_API_URL=http://localhost:5000/api
```

---

## 📁 Project Structure

```
project 2/
├── backend/              # Flask API
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── models/      # Database models
│   │   ├── services/    # Business logic
│   │   └── utils/       # Utilities
│   ├── run.py           # Entry point
│   └── requirements.txt
│
└── frontend/            # React App
    ├── src/
    │   ├── components/  # UI components
    │   ├── pages/       # Pages
    │   ├── context/     # State management
    │   └── services/    # API calls
    ├── package.json
    └── vite.config.js
```

---

## 🧪 Testing the API

### Using cURL

```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"Test1234"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"Test1234"}'

# Get expenses (replace TOKEN)
curl -X GET http://localhost:5000/api/expenses/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Using Postman

1. Import collection from `docs/postman_collection.json` (if created)
2. Set base URL: `http://localhost:5000/api`
3. Test endpoints

---

## 🐛 Troubleshooting

### Backend Issues

**Port already in use**:
```bash
# Change port in run.py
app.run(port=5001)
```

**Database errors**:
```bash
# Reset database
rm expenses.db
flask db upgrade
```

**Module not found**:
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Issues

**Port already in use**:
```javascript
// Change port in vite.config.js
server: { port: 3001 }
```

**API connection failed**:
```bash
# Check VITE_API_URL in .env
# Ensure backend is running
```

**Build errors**:
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install
```

---

## 📊 Key Features to Test

### 1. Expense Management
- ✅ Add expense
- ✅ Edit expense
- ✅ Delete expense
- ✅ Filter by date/category
- ✅ Export to CSV

### 2. Analytics
- ✅ Monthly summary
- ✅ Category breakdown
- ✅ Spending trends
- ✅ AI insights
- ✅ Predictions

### 3. Budget
- ✅ Set monthly budget
- ✅ Set monthly income
- ✅ View budget progress
- ✅ Budget alerts

---

## 🎨 Customization

### Change Theme Colors

Edit `frontend/tailwind.config.js`:
```javascript
colors: {
  primary: {
    500: '#your-color',
    600: '#your-darker-color',
  }
}
```

### Add New Category

Edit `backend/app/models/expense.py`:
```python
CATEGORIES = ['Food', 'Travel', 'Shopping', 'Bills', 'Entertainment', 'Your-Category']
```

---

## 📚 Next Steps

1. **Read Documentation**:
   - `UPGRADE_GUIDE.md` - Detailed changes
   - `API_DOCUMENTATION.md` - API reference
   - `DEPLOYMENT_GUIDE.md` - Deploy to production

2. **Explore Code**:
   - Backend: Start with `backend/app/api/`
   - Frontend: Start with `frontend/src/pages/`

3. **Add Features**:
   - Implement recurring expenses
   - Add more chart types
   - Create mobile app

4. **Deploy**:
   - Follow `DEPLOYMENT_GUIDE.md`
   - Deploy backend to Render
   - Deploy frontend to Vercel

---

## 🆘 Getting Help

### Documentation
- `TRANSFORMATION_SUMMARY.md` - Overview of changes
- `UPGRADE_GUIDE.md` - Migration guide
- `API_DOCUMENTATION.md` - API reference

### Common Questions

**Q: How do I add a new API endpoint?**
A: Create route in `backend/app/api/`, add service in `backend/app/services/`

**Q: How do I add a new page?**
A: Create component in `frontend/src/pages/`, add route in `App.jsx`

**Q: How do I change the database?**
A: Update `DATABASE_URL` in `.env`, run migrations

**Q: How do I add authentication to a new endpoint?**
A: Add `@jwt_required()` decorator to the route

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Backend running on port 5000
- [ ] Frontend running on port 3000
- [ ] Can register new user
- [ ] Can login
- [ ] Can add expense
- [ ] Can view analytics
- [ ] Can export CSV
- [ ] No console errors

---

## 🎉 You're Ready!

Your ExpenseSense Pro v2.0 is now running locally. Start building amazing features!

**Happy Coding! 🚀**

---

**Version**: 2.0.0  
**Last Updated**: April 2026  
**Support**: Check documentation files for detailed guides

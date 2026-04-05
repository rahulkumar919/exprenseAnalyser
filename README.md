# ExpenseSense Pro - Expense Tracking Application

A full-stack expense tracking application with AI-powered insights, receipt scanning, and smart budgeting tools.

## 🏗️ Architecture Overview

### Backend (Python Flask)
```
app.py                    # Main Flask application entry point
├── models/
│   └── database.py       # SQLite database connection & schema
├── routes/               # API endpoints (Blueprint pattern)
│   ├── auth.py          # User authentication (signup/login/logout)
│   ├── expense.py       # CRUD operations for expenses
│   ├── analysis.py      # Data analysis & insights (pandas)
│   ├── smart.py         # Recipe & travel budget estimators
│   └── ocr.py           # Receipt scanning with EasyOCR
└── expenses.db          # SQLite database file
```

### Frontend (Vanilla JavaScript + Chart.js)
```
templates/
├── index.html           # Main dashboard (SPA-style)
└── login.html           # Authentication page

static/
├── css/
│   └── style.css        # Modern glassmorphism design
└── js/
    └── script.js        # Client-side logic, API calls, charts
```

### Database Schema (SQLite)
- **users**: id, username, email, password (hashed)
- **expenses**: id, user_id, date, amount, category, description
- **budgets**: id, user_id, monthly_budget

### Key Features
1. **Expense Tracking**: Add, edit, delete expenses with categories
2. **Visual Analytics**: Chart.js pie charts and line graphs
3. **Budget Management**: Set monthly budgets with progress tracking
4. **Receipt OCR**: Scan receipts using EasyOCR (extracts amount, date, description)
5. **Smart Tools**:
   - Recipe Budget Estimator (Maggi, Paneer, Pasta, Chai)
   - Travel Budget Planner (destination-based cost estimation)
6. **AI Insights**: Spending pattern analysis using pandas
7. **Theme Toggle**: Dark/Light mode with localStorage persistence

### Technology Stack
- **Backend**: Flask 3.1.3, SQLite3, Flask-CORS
- **ML/Data**: pandas, numpy, scikit-learn, EasyOCR, torch
- **Frontend**: Vanilla JS, Chart.js, Font Awesome
- **Build Tools**: npm, ESBuild, PostCSS, Prettier, ESLint

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+ installed
- Node.js 16+ and npm installed
- pip (Python package manager)

### Step 1: Install Python Dependencies
```bash
cd "project 2"
pip install -r requirements.txt
```

**Note**: This will install ~100+ packages including:
- Flask, Flask-CORS
- pandas, numpy, scikit-learn
- EasyOCR, torch, torchvision (for receipt scanning)
- Pillow, opencv-python-headless
- And many more data science libraries

**Installation may take 5-10 minutes** depending on your internet speed.

### Step 2: Install Node.js Dependencies (Optional)
```bash
npm install
```

This installs frontend build tools:
- ESBuild (JS bundler)
- PostCSS (CSS processor)
- ESLint, Stylelint, Prettier (code quality)

### Step 3: Initialize Database
The database will be created automatically on first run. To manually initialize:
```python
python -c "from models.database import init_db; init_db()"
```

### Step 4: Run the Application
```bash
# Using npm script (recommended)
npm run dev

# Or directly with Python
python app.py
```

The app will start on **http://localhost:5000**

---

## 📋 Available npm Scripts

```bash
npm run dev              # Start Flask development server
npm run start            # Alias for dev
npm run install-python   # Install Python dependencies via pip

# Build & Watch (for production)
npm run build            # Minify CSS & bundle JS
npm run build:css        # Build CSS only
npm run build:js         # Build JS only
npm run watch            # Auto-rebuild on file changes
npm run watch:css        # Watch CSS changes
npm run watch:js         # Watch JS changes

# Code Quality
npm run lint             # Run ESLint + Stylelint
npm run lint:js          # Lint JavaScript files
npm run lint:css         # Lint CSS files
npm run format           # Format code with Prettier
```

---

## 🔑 Usage Flow

1. **First Time Setup**:
   - Navigate to `/login`
   - Click "Sign Up" and create an account
   - Login with your credentials

2. **Dashboard**:
   - Set your monthly budget and income
   - Add expenses manually or scan receipts
   - View real-time charts and analytics
   - Use smart tools (recipe estimator, travel planner)

3. **Receipt Scanning**:
   - Click "Scan Receipt" button
   - Upload an image of your receipt
   - EasyOCR extracts amount, date, and description
   - Review and submit the expense

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'pandas'`
**Solution**: Run `pip install -r requirements.txt`

### Issue: Port 5000 already in use
**Solution**: Change port in `app.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

### Issue: EasyOCR not working
**Solution**: EasyOCR requires torch. Ensure you have enough disk space (~2GB for models)

### Issue: Database locked error
**Solution**: Close any other connections to `expenses.db` and restart the app

---

## 🔒 Security Notes

- Passwords are hashed using `werkzeug.security`
- Session management with Flask sessions
- CORS enabled for development (restrict in production)
- **TODO**: Add JWT authentication for production
- **TODO**: Use environment variables for `app.secret_key`

---

## 📦 Production Deployment

1. Set `debug=False` in `app.py`
2. Use a production WSGI server (gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
3. Serve static files via Nginx/Apache
4. Use PostgreSQL instead of SQLite for scalability
5. Add HTTPS with SSL certificates

---

## 📄 License
MIT License

## 👨‍💻 Contributing
Pull requests welcome! Please follow the existing code style.

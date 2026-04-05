# 📁 Expense Analyser Pro - Project Structure

## Overview
A modern, full-stack expense tracking application with AI-powered insights, receipt OCR scanning, and smart budgeting tools.

---

## Directory Structure

```
project 2/
├── 📄 app.py                          # Flask application entry point
├── 📄 expenses.db                     # SQLite database (auto-generated)
├── 📄 requirements.txt                # Python dependencies
├── 📄 package.json                    # Node.js dependencies & scripts
├── 📄 postcss.config.js               # PostCSS configuration
├── 📄 .eslintrc.json                  # ESLint configuration
├── 📄 .stylelintrc.json               # Stylelint configuration
├── 📄 .prettierrc                     # Prettier configuration
├── 📄 .gitignore                      # Git ignore rules
├── 📄 README.md                       # Project documentation
├── 📄 QUICKSTART.md                   # Quick start guide
├── 📄 DESIGN_SYSTEM.md                # Design system documentation
├── 📄 PROJECT_STRUCTURE.md            # This file
│
├── 📁 models/                         # Database models
│   ├── 📄 database.py                 # DB connection & schema
│   └── 📁 __pycache__/                # Python cache
│
├── 📁 routes/                         # API endpoints (Blueprints)
│   ├── 📄 auth.py                     # Authentication routes
│   ├── 📄 expense.py                  # Expense CRUD operations
│   ├── 📄 analysis.py                 # Data analysis & insights
│   ├── 📄 smart.py                    # Smart tools (recipe, travel)
│   ├── 📄 ocr.py                      # Receipt scanning
│   └── 📁 __pycache__/                # Python cache
│
├── 📁 templates/                      # HTML templates
│   ├── 📄 index.html                  # Main dashboard
│   └── 📄 login.html                  # Authentication page
│
├── 📁 static/                         # Static assets
│   ├── 📁 css/
│   │   ├── 📄 style.css               # Main stylesheet
│   │   └── 📄 style.min.css           # Minified CSS (build output)
│   └── 📁 js/
│       ├── 📄 script.js               # Main JavaScript
│       └── 📄 script.min.js           # Minified JS (build output)
│
└── 📁 node_modules/                   # npm packages (after install)
```

---

## File Descriptions

### Root Files

#### `app.py`
Main Flask application file that:
- Initializes Flask app with CORS
- Registers all Blueprint routes
- Initializes database on first run
- Serves HTML templates
- Runs development server on port 5000

#### `requirements.txt`
Python dependencies including:
- Flask 3.1.3 (web framework)
- pandas, numpy (data analysis)
- EasyOCR, torch (receipt scanning)
- scikit-learn (ML predictions)
- And 100+ other packages

#### `package.json`
Node.js configuration with scripts:
- `npm run dev` - Start Flask server
- `npm run build` - Minify CSS/JS
- `npm run watch` - Auto-rebuild on changes
- `npm run lint` - Code quality checks
- `npm run format` - Code formatting

---

### Models Directory

#### `models/database.py`
Database layer containing:
- `get_db_connection()` - SQLite connection helper
- `init_db()` - Creates tables on first run

**Database Schema:**
```sql
users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT  -- hashed with werkzeug
)

expenses (
    id INTEGER PRIMARY KEY,
    user_id INTEGER FOREIGN KEY,
    date TEXT,
    amount REAL,
    category TEXT,
    description TEXT
)

budgets (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE FOREIGN KEY,
    monthly_budget REAL DEFAULT 0
)
```

---

### Routes Directory (API Endpoints)

#### `routes/auth.py`
Authentication endpoints:
- `POST /signup` - Create new user
- `POST /login` - Authenticate user
- `POST /logout` - Clear session

#### `routes/expense.py`
Expense management:
- `POST /add_expense` - Create expense
- `GET /expenses/<user_id>` - List all expenses
- `PUT /update_expense/<id>` - Update expense
- `DELETE /delete_expense/<id>` - Delete expense

#### `routes/analysis.py`
Data analysis (uses pandas):
- Spending pattern analysis
- Category-wise breakdowns
- Trend predictions
- AI-powered insights

#### `routes/smart.py`
Smart tools:
- `GET /recipe/<name>` - Recipe cost estimator
- `POST /travel` - Travel budget planner
- `POST /set_budget` - Set monthly budget
- `GET /budget/<user_id>` - Get budget info

#### `routes/ocr.py`
Receipt scanning:
- `POST /scan_receipt` - Upload & scan receipt
- Uses EasyOCR to extract:
  - Amount
  - Date
  - Description/Merchant

---

### Templates Directory

#### `templates/index.html`
Main dashboard (SPA-style) with:
- Hero section with animated title
- Budget & income inputs
- 4 stat cards (balance, expenses, spending, projection)
- AI insights section
- Smart tools (recipe estimator, travel planner)
- Charts (pie chart, line chart)
- Add expense form with OCR upload
- Transactions table
- Features showcase section

#### `templates/login.html`
Authentication page with:
- Login form
- Signup form
- Form validation
- Session management

---

### Static Directory

#### `static/css/style.css`
Main stylesheet (2000+ lines) with:
- CSS custom properties (design tokens)
- Dark/Light theme support
- Glassmorphism effects
- Responsive grid layouts
- Smooth animations
- Component styles
- Utility classes

**Key Sections:**
1. CSS Variables (colors, spacing, typography)
2. Global styles (reset, body, html)
3. Background animations (blobs, gradients)
4. Layout components (header, dashboard, grids)
5. UI components (cards, buttons, forms, tables)
6. Animations & transitions
7. Responsive breakpoints
8. Accessibility features

#### `static/js/script.js`
Client-side logic (800+ lines) with:
- State management
- API calls (fetch)
- Chart.js integration
- Form handling
- OCR upload
- Theme toggle
- Local storage
- DOM manipulation
- Event listeners

**Key Features:**
- Expense CRUD operations
- Real-time chart updates
- Budget progress tracking
- Recipe cost calculator
- Travel budget estimator
- Receipt scanning
- Theme persistence
- Smooth animations

---

## Data Flow

### 1. User Authentication
```
User → login.html → POST /login → Session → Redirect to index.html
```

### 2. Add Expense
```
User fills form → POST /add_expense → SQLite → Reload data → Update UI
```

### 3. Receipt Scanning
```
User uploads image → POST /scan_receipt → EasyOCR → Extract data → Autofill form
```

### 4. Budget Tracking
```
User sets budget → POST /set_budget → SQLite → Calculate progress → Update UI
```

### 5. Smart Tools
```
User selects recipe → GET /recipe/<name> → Return cost → Display result
User enters destination → POST /travel → Calculate estimate → Display result
```

---

## Technology Stack

### Backend
- **Framework**: Flask 3.1.3
- **Database**: SQLite3
- **ORM**: Raw SQL (sqlite3 module)
- **Auth**: werkzeug.security (password hashing)
- **CORS**: Flask-CORS

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Custom properties, Grid, Flexbox
- **JavaScript**: ES6+ (vanilla, no framework)
- **Charts**: Chart.js 3.x
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Google Fonts (Poppins, JetBrains Mono)

### Data Science
- **pandas**: Data manipulation
- **numpy**: Numerical operations
- **scikit-learn**: ML predictions
- **EasyOCR**: Receipt text extraction
- **torch**: Deep learning backend

### Build Tools
- **npm**: Package management
- **ESBuild**: JavaScript bundler
- **PostCSS**: CSS processor
- **Autoprefixer**: CSS vendor prefixes
- **cssnano**: CSS minification
- **ESLint**: JavaScript linting
- **Stylelint**: CSS linting
- **Prettier**: Code formatting

---

## Development Workflow

### 1. Initial Setup
```bash
pip install -r requirements.txt  # Install Python deps
npm install                       # Install Node deps
```

### 2. Development
```bash
npm run dev                       # Start Flask server
# OR
python app.py                     # Direct Python execution
```

### 3. Building for Production
```bash
npm run build                     # Minify CSS & JS
```

### 4. Code Quality
```bash
npm run lint                      # Check code quality
npm run format                    # Format code
```

---

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/signup` | Create new user |
| POST | `/login` | Authenticate user |
| POST | `/logout` | Clear session |
| POST | `/add_expense` | Create expense |
| GET | `/expenses/<user_id>` | List expenses |
| PUT | `/update_expense/<id>` | Update expense |
| DELETE | `/delete_expense/<id>` | Delete expense |
| GET | `/recipe/<name>` | Get recipe cost |
| POST | `/travel` | Calculate travel budget |
| POST | `/set_budget` | Set monthly budget |
| GET | `/budget/<user_id>` | Get budget info |
| POST | `/scan_receipt` | OCR receipt scan |

---

## Database Tables

### users
- Stores user credentials
- Password hashed with werkzeug
- Unique username & email

### expenses
- Tracks all transactions
- Linked to user via foreign key
- Stores date, amount, category, description

### budgets
- One budget per user
- Stores monthly budget limit
- Used for progress tracking

---

## Key Features

1. ✅ User authentication (signup/login)
2. ✅ Expense tracking (CRUD operations)
3. ✅ Budget management with progress bars
4. ✅ Visual analytics (Chart.js)
5. ✅ Receipt OCR scanning (EasyOCR)
6. ✅ Recipe cost estimator
7. ✅ Travel budget planner
8. ✅ AI spending insights (pandas)
9. ✅ Dark/Light theme toggle
10. ✅ Responsive design
11. ✅ Smooth animations
12. ✅ Glassmorphism UI

---

## Performance Optimizations

- Hardware-accelerated CSS animations
- Debounced scroll events
- Lazy loading for images
- Minified CSS & JS in production
- Efficient SQL queries
- Local storage for theme/session
- Chart.js canvas rendering

---

## Security Considerations

- ✅ Password hashing (werkzeug)
- ✅ Session management (Flask sessions)
- ✅ SQL injection prevention (parameterized queries)
- ⚠️ TODO: HTTPS in production
- ⚠️ TODO: JWT authentication
- ⚠️ TODO: Rate limiting
- ⚠️ TODO: CSRF protection
- ⚠️ TODO: Environment variables for secrets

---

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

## Future Enhancements

- [ ] Export data (CSV, PDF)
- [ ] Recurring expenses
- [ ] Multiple currencies
- [ ] Email notifications
- [ ] Mobile app (React Native)
- [ ] Social sharing
- [ ] Expense categories customization
- [ ] Multi-user households
- [ ] Bank account integration
- [ ] Investment tracking

---

**Version**: 2.0  
**Last Updated**: 2024  
**Maintainer**: Development Team

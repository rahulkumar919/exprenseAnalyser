# ExpenseSense Pro - API Documentation

## Base URL
```
Development: http://localhost:5000/api
Production: https://your-api.com/api
```

## Authentication

All endpoints except `/auth/register` and `/auth/login` require authentication.

**Header Format:**
```
Authorization: Bearer <access_token>
```

---

## 🔐 Authentication Endpoints

### Register User
```http
POST /auth/register
```

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "is_active": true,
    "is_verified": false,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

**Errors:**
- `400`: Invalid input or user already exists

---

### Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "SecurePass123"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "is_active": true
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Errors:**
- `401`: Invalid credentials
- `400`: Missing fields

---

### Refresh Token
```http
POST /auth/refresh
Authorization: Bearer <refresh_token>
```

**Response (200):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### Get Current User
```http
GET /auth/me
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

## 💰 Expenses Endpoints

### List Expenses
```http
GET /expenses/?page=1&per_page=20&category=Food&start_date=2024-01-01
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 20, max: 100)
- `category` (optional): Filter by category
- `start_date` (optional): Filter from date (ISO format)
- `end_date` (optional): Filter to date (ISO format)
- `min_amount` (optional): Minimum amount
- `max_amount` (optional): Maximum amount

**Response (200):**
```json
{
  "expenses": [
    {
      "id": 1,
      "user_id": 1,
      "amount": 250.50,
      "category": "Food",
      "description": "Grocery shopping",
      "date": "2024-01-15",
      "is_recurring": false,
      "recurring_frequency": null,
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00"
    }
  ],
  "total": 45,
  "pages": 3,
  "current_page": 1,
  "per_page": 20
}
```

---

### Create Expense
```http
POST /expenses/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "amount": 250.50,
  "category": "Food",
  "description": "Grocery shopping",
  "date": "2024-01-15",
  "is_recurring": false,
  "recurring_frequency": null
}
```

**Response (201):**
```json
{
  "message": "Expense created successfully",
  "expense": {
    "id": 1,
    "amount": 250.50,
    "category": "Food",
    "description": "Grocery shopping",
    "date": "2024-01-15"
  }
}
```

**Errors:**
- `400`: Invalid input

---

### Get Single Expense
```http
GET /expenses/<id>
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "expense": {
    "id": 1,
    "amount": 250.50,
    "category": "Food",
    "description": "Grocery shopping",
    "date": "2024-01-15"
  }
}
```

**Errors:**
- `404`: Expense not found

---

### Update Expense
```http
PUT /expenses/<id>
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "amount": 300.00,
  "description": "Updated description"
}
```

**Response (200):**
```json
{
  "message": "Expense updated successfully",
  "expense": {
    "id": 1,
    "amount": 300.00,
    "description": "Updated description"
  }
}
```

---

### Delete Expense
```http
DELETE /expenses/<id>
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "message": "Expense deleted successfully"
}
```

---

### Export Expenses (CSV)
```http
GET /expenses/export?start_date=2024-01-01&end_date=2024-01-31
Authorization: Bearer <access_token>
```

**Response (200):**
```csv
Date,Category,Description,Amount
2024-01-15,Food,Grocery shopping,250.50
2024-01-16,Travel,Uber ride,45.00
```

---

## 📊 Analytics Endpoints

### Get Monthly Summary
```http
GET /analytics/summary?year=2024&month=1
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "year": 2024,
  "month": 1,
  "total_expenses": 5420.50,
  "budget": 10000.00,
  "income": 15000.00,
  "balance": 9579.50,
  "budget_used_percentage": 54.21,
  "categories": {
    "Food": 1500.00,
    "Travel": 800.00,
    "Shopping": 2000.00
  },
  "expense_count": 45
}
```

---

### Get Spending Trends
```http
GET /analytics/trends?months=6
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "trends": [
    {
      "year": 2024,
      "month": 1,
      "total": 5420.50,
      "month_name": "January 2024"
    },
    {
      "year": 2024,
      "month": 2,
      "total": 6100.00,
      "month_name": "February 2024"
    }
  ]
}
```

---

### Get Category Breakdown
```http
GET /analytics/category-breakdown?start_date=2024-01-01&end_date=2024-01-31
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "categories": [
    {
      "category": "Food",
      "total": 1500.00,
      "count": 15
    },
    {
      "category": "Travel",
      "total": 800.00,
      "count": 8
    }
  ]
}
```

---

### Get Category Trends
```http
GET /analytics/category-trends/Food?months=6
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "category": "Food",
  "trends": [
    {
      "year": 2024,
      "month": 1,
      "total": 1500.00,
      "month_name": "January 2024"
    }
  ]
}
```

---

### Get Spending Prediction
```http
GET /analytics/prediction
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "predicted_amount": 5800.50,
  "month": "next_month"
}
```

---

### Get AI Insights
```http
GET /analytics/insights
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "insights": [
    {
      "type": "warning",
      "category": "budget",
      "message": "You've used 85.5% of your monthly budget!",
      "suggestion": "Consider reducing non-essential expenses."
    },
    {
      "type": "info",
      "category": "spending_pattern",
      "message": "Food accounts for 45.2% of your spending.",
      "suggestion": "Consider if you can optimize Food expenses."
    }
  ]
}
```

---

### Get Spending Heatmap
```http
GET /analytics/heatmap?year=2024
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "heatmap": {
    "2024-01-15": 250.50,
    "2024-01-16": 450.00,
    "2024-01-17": 120.00
  }
}
```

---

## 💵 Budget Endpoints

### Get Budget
```http
GET /budget/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "budget": {
    "id": 1,
    "user_id": 1,
    "monthly_budget": 10000.00,
    "monthly_income": 15000.00,
    "currency": "INR",
    "alert_threshold": 80.0,
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

---

### Update Budget
```http
PUT /budget/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "monthly_budget": 12000.00,
  "monthly_income": 18000.00,
  "currency": "INR",
  "alert_threshold": 85.0
}
```

**Response (200):**
```json
{
  "message": "Budget updated successfully",
  "budget": {
    "monthly_budget": 12000.00,
    "monthly_income": 18000.00
  }
}
```

---

## 👤 User Endpoints

### Get Profile
```http
GET /users/profile
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

### Update Profile
```http
PUT /users/profile
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "email": "newemail@example.com"
}
```

**Response (200):**
```json
{
  "message": "Profile updated successfully",
  "user": {
    "email": "newemail@example.com"
  }
}
```

---

## ⚠️ Error Responses

### Standard Error Format
```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

### Common Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `429`: Rate Limit Exceeded
- `500`: Internal Server Error

---

## 🔒 Rate Limits

- **Authentication**: 5 requests/hour (register), 10 requests/minute (login)
- **Expenses**: 30 requests/minute (write), 100 requests/minute (read)
- **Analytics**: 60 requests/minute
- **Export**: 10 requests/hour

---

## 📝 Notes

1. All dates should be in ISO format: `YYYY-MM-DD`
2. All timestamps are in UTC
3. Amounts are in float format with 2 decimal places
4. Access tokens expire after 1 hour
5. Refresh tokens expire after 30 days

---

**API Version**: 2.0  
**Last Updated**: April 2026

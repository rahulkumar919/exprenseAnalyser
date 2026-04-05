"""Analytics service layer with AI insights."""
from app import db
from app.models.expense import Expense
from app.models.budget import Budget
from sqlalchemy import func, extract
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import numpy as np


class AnalyticsService:
    """Service for analytics and AI insights."""
    
    @staticmethod
    def get_monthly_summary(user_id, year=None, month=None):
        """Get monthly expense summary."""
        if not year:
            year = datetime.now().year
        if not month:
            month = datetime.now().month
        
        # Get expenses for the month
        expenses = Expense.query.filter(
            Expense.user_id == user_id,
            extract('year', Expense.date) == year,
            extract('month', Expense.date) == month
        ).all()
        
        total = sum(e.amount for e in expenses)
        
        # Category breakdown
        categories = {}
        for expense in expenses:
            if expense.category not in categories:
                categories[expense.category] = 0
            categories[expense.category] += expense.amount
        
        # Get budget
        budget = Budget.query.filter_by(user_id=user_id).first()
        budget_amount = budget.monthly_budget if budget else 0
        income = budget.monthly_income if budget else 0
        
        return {
            'year': year,
            'month': month,
            'total_expenses': total,
            'budget': budget_amount,
            'income': income,
            'balance': income - total,
            'budget_used_percentage': (total / budget_amount * 100) if budget_amount > 0 else 0,
            'categories': categories,
            'expense_count': len(expenses)
        }
    
    @staticmethod
    def get_spending_trends(user_id, months=6):
        """Get spending trends for last N months."""
        end_date = date.today()
        start_date = end_date - relativedelta(months=months)
        
        # Query expenses grouped by month
        results = db.session.query(
            extract('year', Expense.date).label('year'),
            extract('month', Expense.date).label('month'),
            func.sum(Expense.amount).label('total')
        ).filter(
            Expense.user_id == user_id,
            Expense.date >= start_date,
            Expense.date <= end_date
        ).group_by('year', 'month').order_by('year', 'month').all()
        
        trends = []
        for row in results:
            trends.append({
                'year': int(row.year),
                'month': int(row.month),
                'total': float(row.total),
                'month_name': datetime(int(row.year), int(row.month), 1).strftime('%B %Y')
            })
        
        return trends
    
    @staticmethod
    def predict_next_month_spending(user_id):
        """Predict next month spending using simple moving average."""
        # Get last 3 months data
        trends = AnalyticsService.get_spending_trends(user_id, months=3)
        
        if len(trends) < 2:
            return 0.0
        
        # Simple moving average
        amounts = [t['total'] for t in trends]
        prediction = np.mean(amounts)
        
        # Add 5% buffer for safety
        prediction *= 1.05
        
        return round(prediction, 2)
    
    @staticmethod
    def get_category_trends(user_id, category, months=6):
        """Get spending trend for specific category."""
        end_date = date.today()
        start_date = end_date - relativedelta(months=months)
        
        results = db.session.query(
            extract('year', Expense.date).label('year'),
            extract('month', Expense.date).label('month'),
            func.sum(Expense.amount).label('total')
        ).filter(
            Expense.user_id == user_id,
            Expense.category == category,
            Expense.date >= start_date,
            Expense.date <= end_date
        ).group_by('year', 'month').order_by('year', 'month').all()
        
        trends = []
        for row in results:
            trends.append({
                'year': int(row.year),
                'month': int(row.month),
                'total': float(row.total),
                'month_name': datetime(int(row.year), int(row.month), 1).strftime('%B %Y')
            })
        
        return trends
    
    @staticmethod
    def get_ai_insights(user_id):
        """Generate AI-powered financial insights."""
        insights = []
        
        # Get current month data
        current_month = AnalyticsService.get_monthly_summary(user_id)
        
        # Budget alert
        if current_month['budget'] > 0:
            usage_pct = current_month['budget_used_percentage']
            if usage_pct > 90:
                insights.append({
                    'type': 'warning',
                    'category': 'budget',
                    'message': f"You've used {usage_pct:.1f}% of your monthly budget!",
                    'suggestion': "Consider reducing non-essential expenses."
                })
            elif usage_pct > 75:
                insights.append({
                    'type': 'info',
                    'category': 'budget',
                    'message': f"You've used {usage_pct:.1f}% of your budget.",
                    'suggestion': "Monitor your spending closely for the rest of the month."
                })
        
        # Category analysis
        categories = current_month['categories']
        if categories:
            max_category = max(categories, key=categories.get)
            max_amount = categories[max_category]
            total = current_month['total_expenses']
            
            if total > 0:
                pct = (max_amount / total) * 100
                if pct > 40:
                    insights.append({
                        'type': 'info',
                        'category': 'spending_pattern',
                        'message': f"{max_category} accounts for {pct:.1f}% of your spending.",
                        'suggestion': f"Consider if you can optimize {max_category} expenses."
                    })
        
        # Spending trend
        trends = AnalyticsService.get_spending_trends(user_id, months=3)
        if len(trends) >= 2:
            last_month = trends[-1]['total']
            prev_month = trends[-2]['total']
            change = ((last_month - prev_month) / prev_month) * 100 if prev_month > 0 else 0
            
            if change > 20:
                insights.append({
                    'type': 'warning',
                    'category': 'trend',
                    'message': f"Your spending increased by {change:.1f}% last month.",
                    'suggestion': "Review your recent expenses to identify the cause."
                })
            elif change < -20:
                insights.append({
                    'type': 'success',
                    'category': 'trend',
                    'message': f"Great job! Your spending decreased by {abs(change):.1f}% last month.",
                    'suggestion': "Keep up the good work!"
                })
        
        # Savings rate
        if current_month['income'] > 0:
            savings_rate = (current_month['balance'] / current_month['income']) * 100
            if savings_rate < 10:
                insights.append({
                    'type': 'warning',
                    'category': 'savings',
                    'message': f"Your savings rate is only {savings_rate:.1f}%.",
                    'suggestion': "Aim to save at least 20% of your income."
                })
            elif savings_rate > 30:
                insights.append({
                    'type': 'success',
                    'category': 'savings',
                    'message': f"Excellent! You're saving {savings_rate:.1f}% of your income.",
                    'suggestion': "Consider investing your savings for long-term growth."
                })
        
        return insights
    
    @staticmethod
    def get_spending_heatmap(user_id, year=None):
        """Get daily spending heatmap for the year."""
        if not year:
            year = datetime.now().year
        
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        
        results = db.session.query(
            Expense.date,
            func.sum(Expense.amount).label('total')
        ).filter(
            Expense.user_id == user_id,
            Expense.date >= start_date,
            Expense.date <= end_date
        ).group_by(Expense.date).all()
        
        heatmap = {}
        for row in results:
            heatmap[row.date.isoformat()] = float(row.total)
        
        return heatmap

"""Expense service layer."""
from app import db
from app.models.expense import Expense
from datetime import datetime, date
from sqlalchemy import and_, extract, func


class ExpenseService:
    """Service for expense operations."""
    
    @staticmethod
    def create_expense(user_id, amount, category, description, expense_date, 
                      is_recurring=False, recurring_frequency=None):
        """Create a new expense."""
        expense = Expense(
            user_id=user_id,
            amount=amount,
            category=category,
            description=description,
            date=expense_date,
            is_recurring=is_recurring,
            recurring_frequency=recurring_frequency
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return expense
    
    @staticmethod
    def get_user_expenses(user_id, page=1, per_page=20, filters=None):
        """Get user expenses with pagination and filters."""
        query = Expense.query.filter_by(user_id=user_id)
        
        # Apply filters
        if filters:
            if 'category' in filters:
                query = query.filter_by(category=filters['category'])
            
            if 'start_date' in filters:
                query = query.filter(Expense.date >= filters['start_date'])
            
            if 'end_date' in filters:
                query = query.filter(Expense.date <= filters['end_date'])
            
            if 'min_amount' in filters:
                query = query.filter(Expense.amount >= filters['min_amount'])
            
            if 'max_amount' in filters:
                query = query.filter(Expense.amount <= filters['max_amount'])
        
        # Order by date descending
        query = query.order_by(Expense.date.desc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'expenses': [expense.to_dict() for expense in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }
    
    @staticmethod
    def get_expense_by_id(expense_id, user_id):
        """Get expense by ID for specific user."""
        return Expense.query.filter_by(id=expense_id, user_id=user_id).first()
    
    @staticmethod
    def update_expense(expense_id, user_id, **kwargs):
        """Update expense."""
        expense = ExpenseService.get_expense_by_id(expense_id, user_id)
        
        if not expense:
            raise ValueError("Expense not found")
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(expense, key) and value is not None:
                setattr(expense, key, value)
        
        db.session.commit()
        return expense
    
    @staticmethod
    def delete_expense(expense_id, user_id):
        """Delete expense."""
        expense = ExpenseService.get_expense_by_id(expense_id, user_id)
        
        if not expense:
            raise ValueError("Expense not found")
        
        db.session.delete(expense)
        db.session.commit()
        
        return True
    
    @staticmethod
    def get_total_expenses(user_id, start_date=None, end_date=None):
        """Get total expenses for user in date range."""
        query = db.session.query(func.sum(Expense.amount)).filter_by(user_id=user_id)
        
        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)
        
        total = query.scalar()
        return total or 0.0
    
    @staticmethod
    def get_category_breakdown(user_id, start_date=None, end_date=None):
        """Get expenses grouped by category."""
        query = db.session.query(
            Expense.category,
            func.sum(Expense.amount).label('total'),
            func.count(Expense.id).label('count')
        ).filter_by(user_id=user_id)
        
        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)
        
        results = query.group_by(Expense.category).all()
        
        return [
            {
                'category': row.category,
                'total': float(row.total),
                'count': row.count
            }
            for row in results
        ]
    
    @staticmethod
    def export_expenses_csv(user_id, start_date=None, end_date=None):
        """Export expenses to CSV format."""
        query = Expense.query.filter_by(user_id=user_id)
        
        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)
        
        expenses = query.order_by(Expense.date.desc()).all()
        
        # Create CSV data
        csv_data = "Date,Category,Description,Amount\n"
        for expense in expenses:
            csv_data += f"{expense.date},{expense.category},{expense.description or ''},{expense.amount}\n"
        
        return csv_data

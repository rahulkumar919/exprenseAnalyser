"""Expense model."""
from datetime import datetime
from app import db


class Expense(db.Model):
    """Expense model."""
    
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.String(255))
    date = db.Column(db.Date, nullable=False, index=True)
    is_recurring = db.Column(db.Boolean, default=False)
    recurring_frequency = db.Column(db.String(20))  # daily, weekly, monthly, yearly
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Expense {self.id}: {self.amount} - {self.category}>'
    
    def to_dict(self):
        """Convert expense to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'is_recurring': self.is_recurring,
            'recurring_frequency': self.recurring_frequency,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ExpenseCategory(db.Model):
    """Expense category model for custom categories."""
    
    __tablename__ = 'expense_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(50))
    color = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'name', name='unique_user_category'),
    )
    
    def to_dict(self):
        """Convert category to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'color': self.color
        }

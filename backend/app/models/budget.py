"""Budget model."""
from datetime import datetime
from app import db


class Budget(db.Model):
    """Budget model."""
    
    __tablename__ = 'budgets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    monthly_budget = db.Column(db.Float, default=0.0)
    monthly_income = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(10), default='INR')
    alert_threshold = db.Column(db.Float, default=80.0)  # Alert at 80% of budget
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Budget user_id={self.user_id}: {self.monthly_budget}>'
    
    def to_dict(self):
        """Convert budget to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'monthly_budget': self.monthly_budget,
            'monthly_income': self.monthly_income,
            'currency': self.currency,
            'alert_threshold': self.alert_threshold,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class CategoryBudget(db.Model):
    """Category-specific budget model."""
    
    __tablename__ = 'category_budgets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    budget_amount = db.Column(db.Float, nullable=False)
    month = db.Column(db.Date, nullable=False)  # First day of the month
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'category', 'month', name='unique_category_budget'),
    )
    
    def to_dict(self):
        """Convert category budget to dictionary."""
        return {
            'id': self.id,
            'category': self.category,
            'budget_amount': self.budget_amount,
            'month': self.month.isoformat() if self.month else None
        }

"""Authentication service layer."""
from flask_jwt_extended import create_access_token, create_refresh_token
from app import db
from app.models.user import User
from app.models.budget import Budget
from datetime import datetime


class AuthService:
    """Service for authentication operations."""
    
    @staticmethod
    def register_user(username, email, password):
        """Register a new user."""
        # Check if user exists
        if User.query.filter_by(username=username).first():
            raise ValueError("Username already exists")
        
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already exists")
        
        # Create user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.flush()  # Get user ID before commit
        
        # Create default budget
        budget = Budget(user_id=user.id)
        db.session.add(budget)
        
        db.session.commit()
        
        return user
    
    @staticmethod
    def authenticate_user(username, password):
        """Authenticate user and return tokens."""
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            raise ValueError("Invalid credentials")
        
        if not user.is_active:
            raise ValueError("Account is deactivated")
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return {
            'user': user.to_dict(include_email=True),
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    
    @staticmethod
    def refresh_access_token(user_id):
        """Create new access token."""
        user = User.query.get(user_id)
        if not user or not user.is_active:
            raise ValueError("Invalid user")
        
        access_token = create_access_token(identity=user_id)
        return access_token
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID."""
        return User.query.get(user_id)

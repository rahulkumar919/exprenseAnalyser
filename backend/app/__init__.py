"""Application factory and extensions."""
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import config
import logging
from logging.handlers import RotatingFileHandler
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


def create_app(config_name='default'):
    """Application factory pattern."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # CORS configuration
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Rate limiting
    if app.config['RATELIMIT_ENABLED']:
        limiter.init_app(app)
    
    # Setup logging
    setup_logging(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # JWT callbacks
    setup_jwt_callbacks(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


def register_blueprints(app):
    """Register application blueprints."""
    from app.api.auth import auth_bp
    from app.api.expenses import expenses_bp
    from app.api.analytics import analytics_bp
    from app.api.budget import budget_bp
    from app.api.users import users_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(expenses_bp, url_prefix='/api/expenses')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(budget_bp, url_prefix='/api/budget')
    app.register_blueprint(users_bp, url_prefix='/api/users')


def register_error_handlers(app):
    """Register error handlers."""
    from app.utils.errors import register_error_handlers as reg_handlers
    reg_handlers(app)


def setup_jwt_callbacks(app):
    """Setup JWT callbacks."""
    from app.utils.jwt_handlers import setup_jwt_handlers
    setup_jwt_handlers(jwt)


def setup_logging(app):
    """Setup application logging."""
    if not app.debug and not app.testing:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # File handler
        file_handler = RotatingFileHandler(
            app.config['LOG_FILE'],
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('ExpenseSense Pro startup')

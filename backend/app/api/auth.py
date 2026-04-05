"""Authentication API routes."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import AuthService
from app.utils.validators import validate_email, validate_password
from app import limiter

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        
        # Validate input
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not username or len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters'}), 400
        
        if not validate_email(email):
            return jsonify({'error': 'Invalid email address'}), 400
        
        password_valid, password_msg = validate_password(password)
        if not password_valid:
            return jsonify({'error': password_msg}), 400
        
        # Register user
        user = AuthService.register_user(username, email, password)
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Registration failed'}), 500


@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """Login user and return JWT tokens."""
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Authenticate
        result = AuthService.authenticate_user(username, password)
        
        return jsonify({
            'message': 'Login successful',
            'user': result['user'],
            'access_token': result['access_token'],
            'refresh_token': result['refresh_token']
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token."""
    try:
        user_id = get_jwt_identity()
        access_token = AuthService.refresh_access_token(user_id)
        
        return jsonify({
            'access_token': access_token
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        return jsonify({'error': 'Token refresh failed'}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user info."""
    try:
        user_id = get_jwt_identity()
        user = AuthService.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict(include_email=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get user info'}), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user (client should delete tokens)."""
    # In a production app, you might want to blacklist the token
    return jsonify({'message': 'Logout successful'}), 200

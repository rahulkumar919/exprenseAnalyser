"""Users API routes."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app import limiter

users_bp = Blueprint('users', __name__)


@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile."""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict(include_email=True)}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch profile'}), 500


@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
@limiter.limit("10 per hour")
def update_profile():
    """Update user profile."""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'email' in data:
            # Check if email already exists
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                return jsonify({'error': 'Email already in use'}), 400
            user.email = data['email']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict(include_email=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to update profile'}), 500

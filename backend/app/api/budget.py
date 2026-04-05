"""Budget API routes."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.budget import Budget
from app import limiter

budget_bp = Blueprint('budget', __name__)


@budget_bp.route('/', methods=['GET'])
@jwt_required()
def get_budget():
    """Get user budget."""
    try:
        user_id = get_jwt_identity()
        budget = Budget.query.filter_by(user_id=user_id).first()
        
        if not budget:
            return jsonify({'error': 'Budget not found'}), 404
        
        return jsonify({'budget': budget.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch budget'}), 500


@budget_bp.route('/', methods=['PUT'])
@jwt_required()
@limiter.limit("30 per minute")
def update_budget():
    """Update user budget."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        budget = Budget.query.filter_by(user_id=user_id).first()
        
        if not budget:
            # Create budget if doesn't exist
            budget = Budget(user_id=user_id)
            db.session.add(budget)
        
        # Update fields
        if 'monthly_budget' in data:
            budget.monthly_budget = float(data['monthly_budget'])
        
        if 'monthly_income' in data:
            budget.monthly_income = float(data['monthly_income'])
        
        if 'currency' in data:
            budget.currency = data['currency']
        
        if 'alert_threshold' in data:
            budget.alert_threshold = float(data['alert_threshold'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Budget updated successfully',
            'budget': budget.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to update budget'}), 500

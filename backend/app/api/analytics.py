"""Analytics API routes."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.analytics_service import AnalyticsService
from app.services.expense_service import ExpenseService
from datetime import datetime
from app import limiter

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/summary', methods=['GET'])
@jwt_required()
@limiter.limit("60 per minute")
def get_summary():
    """Get monthly summary."""
    try:
        user_id = get_jwt_identity()
        
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        
        summary = AnalyticsService.get_monthly_summary(user_id, year, month)
        
        return jsonify(summary), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch summary'}), 500


@analytics_bp.route('/trends', methods=['GET'])
@jwt_required()
@limiter.limit("60 per minute")
def get_trends():
    """Get spending trends."""
    try:
        user_id = get_jwt_identity()
        months = request.args.get('months', 6, type=int)
        months = min(months, 24)  # Max 24 months
        
        trends = AnalyticsService.get_spending_trends(user_id, months)
        
        return jsonify({'trends': trends}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch trends'}), 500


@analytics_bp.route('/category-breakdown', methods=['GET'])
@jwt_required()
@limiter.limit("60 per minute")
def get_category_breakdown():
    """Get category-wise breakdown."""
    try:
        user_id = get_jwt_identity()
        
        start_date = None
        end_date = None
        
        if request.args.get('start_date'):
            start_date = datetime.fromisoformat(request.args.get('start_date')).date()
        
        if request.args.get('end_date'):
            end_date = datetime.fromisoformat(request.args.get('end_date')).date()
        
        breakdown = ExpenseService.get_category_breakdown(user_id, start_date, end_date)
        
        return jsonify({'categories': breakdown}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch category breakdown'}), 500


@analytics_bp.route('/category-trends/<category>', methods=['GET'])
@jwt_required()
@limiter.limit("60 per minute")
def get_category_trends(category):
    """Get trends for specific category."""
    try:
        user_id = get_jwt_identity()
        months = request.args.get('months', 6, type=int)
        
        trends = AnalyticsService.get_category_trends(user_id, category, months)
        
        return jsonify({'category': category, 'trends': trends}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch category trends'}), 500


@analytics_bp.route('/prediction', methods=['GET'])
@jwt_required()
@limiter.limit("30 per minute")
def get_prediction():
    """Get next month spending prediction."""
    try:
        user_id = get_jwt_identity()
        
        prediction = AnalyticsService.predict_next_month_spending(user_id)
        
        return jsonify({
            'predicted_amount': prediction,
            'month': 'next_month'
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to generate prediction'}), 500


@analytics_bp.route('/insights', methods=['GET'])
@jwt_required()
@limiter.limit("30 per minute")
def get_insights():
    """Get AI-powered financial insights."""
    try:
        user_id = get_jwt_identity()
        
        insights = AnalyticsService.get_ai_insights(user_id)
        
        return jsonify({'insights': insights}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to generate insights'}), 500


@analytics_bp.route('/heatmap', methods=['GET'])
@jwt_required()
@limiter.limit("30 per minute")
def get_heatmap():
    """Get spending heatmap."""
    try:
        user_id = get_jwt_identity()
        year = request.args.get('year', type=int)
        
        heatmap = AnalyticsService.get_spending_heatmap(user_id, year)
        
        return jsonify({'heatmap': heatmap}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to generate heatmap'}), 500

"""Expenses API routes."""
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.expense_service import ExpenseService
from datetime import datetime
from app import limiter

expenses_bp = Blueprint('expenses', __name__)


@expenses_bp.route('/', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_expenses():
    """Get user expenses with pagination and filters."""
    try:
        user_id = get_jwt_identity()
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        per_page = min(per_page, 100)  # Max 100 items per page
        
        # Filters
        filters = {}
        if request.args.get('category'):
            filters['category'] = request.args.get('category')
        
        if request.args.get('start_date'):
            filters['start_date'] = datetime.fromisoformat(request.args.get('start_date')).date()
        
        if request.args.get('end_date'):
            filters['end_date'] = datetime.fromisoformat(request.args.get('end_date')).date()
        
        if request.args.get('min_amount'):
            filters['min_amount'] = float(request.args.get('min_amount'))
        
        if request.args.get('max_amount'):
            filters['max_amount'] = float(request.args.get('max_amount'))
        
        result = ExpenseService.get_user_expenses(user_id, page, per_page, filters)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch expenses'}), 500


@expenses_bp.route('/', methods=['POST'])
@jwt_required()
@limiter.limit("30 per minute")
def create_expense():
    """Create a new expense."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        amount = data.get('amount')
        category = data.get('category')
        expense_date = data.get('date')
        
        if not all([amount, category, expense_date]):
            return jsonify({'error': 'Amount, category, and date are required'}), 400
        
        # Parse date
        try:
            expense_date = datetime.fromisoformat(expense_date).date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use ISO format (YYYY-MM-DD)'}), 400
        
        # Validate amount
        try:
            amount = float(amount)
            if amount <= 0:
                return jsonify({'error': 'Amount must be positive'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid amount'}), 400
        
        # Create expense
        expense = ExpenseService.create_expense(
            user_id=user_id,
            amount=amount,
            category=category,
            description=data.get('description', ''),
            expense_date=expense_date,
            is_recurring=data.get('is_recurring', False),
            recurring_frequency=data.get('recurring_frequency')
        )
        
        return jsonify({
            'message': 'Expense created successfully',
            'expense': expense.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to create expense'}), 500


@expenses_bp.route('/<int:expense_id>', methods=['GET'])
@jwt_required()
def get_expense(expense_id):
    """Get a specific expense."""
    try:
        user_id = get_jwt_identity()
        expense = ExpenseService.get_expense_by_id(expense_id, user_id)
        
        if not expense:
            return jsonify({'error': 'Expense not found'}), 404
        
        return jsonify({'expense': expense.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch expense'}), 500


@expenses_bp.route('/<int:expense_id>', methods=['PUT'])
@jwt_required()
@limiter.limit("30 per minute")
def update_expense(expense_id):
    """Update an expense."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Parse date if provided
        if 'date' in data:
            try:
                data['date'] = datetime.fromisoformat(data['date']).date()
            except ValueError:
                return jsonify({'error': 'Invalid date format'}), 400
        
        # Validate amount if provided
        if 'amount' in data:
            try:
                data['amount'] = float(data['amount'])
                if data['amount'] <= 0:
                    return jsonify({'error': 'Amount must be positive'}), 400
            except ValueError:
                return jsonify({'error': 'Invalid amount'}), 400
        
        expense = ExpenseService.update_expense(expense_id, user_id, **data)
        
        return jsonify({
            'message': 'Expense updated successfully',
            'expense': expense.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to update expense'}), 500


@expenses_bp.route('/<int:expense_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("30 per minute")
def delete_expense(expense_id):
    """Delete an expense."""
    try:
        user_id = get_jwt_identity()
        ExpenseService.delete_expense(expense_id, user_id)
        
        return jsonify({'message': 'Expense deleted successfully'}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to delete expense'}), 500


@expenses_bp.route('/export', methods=['GET'])
@jwt_required()
@limiter.limit("10 per hour")
def export_expenses():
    """Export expenses to CSV."""
    try:
        user_id = get_jwt_identity()
        
        # Date filters
        start_date = None
        end_date = None
        
        if request.args.get('start_date'):
            start_date = datetime.fromisoformat(request.args.get('start_date')).date()
        
        if request.args.get('end_date'):
            end_date = datetime.fromisoformat(request.args.get('end_date')).date()
        
        csv_data = ExpenseService.export_expenses_csv(user_id, start_date, end_date)
        
        # Create response with CSV
        response = make_response(csv_data)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=expenses.csv'
        
        return response
        
    except Exception as e:
        return jsonify({'error': 'Failed to export expenses'}), 500

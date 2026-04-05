"""Error handlers."""
from flask import jsonify
from flask_jwt_extended.exceptions import JWTExtendedException
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    """Register error handlers for the application."""
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Forbidden', 'message': 'Access denied'}), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'message': 'Resource not found'}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error': 'Method not allowed'}), 405
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return jsonify({'error': 'Rate limit exceeded', 'message': 'Too many requests'}), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Internal error: {error}')
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(JWTExtendedException)
    def handle_jwt_error(error):
        return jsonify({'error': 'JWT error', 'message': str(error)}), 401
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({'error': error.name, 'message': error.description}), error.code
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f'Unhandled exception: {error}')
        return jsonify({'error': 'An unexpected error occurred'}), 500

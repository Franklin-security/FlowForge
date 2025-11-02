"""
API error handlers for FlowForge.

Provides centralized error handling for API endpoints.
"""

from flask import jsonify
from src.utils.errors import FlowForgeError, ProviderError, ValidationError, AuthenticationError

def register_error_handlers(app):
    """
    Register error handlers for Flask app.
    
    Args:
        app: Flask application instance
    """
    @app.errorhandler(FlowForgeError)
    def handle_flowforge_error(error):
        """Handle FlowForge-specific errors."""
        return jsonify({
            'error': str(error),
            'type': error.__class__.__name__
        }), 400
    
    @app.errorhandler(ProviderError)
    def handle_provider_error(error):
        """Handle provider-related errors."""
        response = {
            'error': str(error),
            'type': 'ProviderError'
        }
        if error.provider_name:
            response['provider'] = error.provider_name
        return jsonify(response), 400
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handle validation errors."""
        return jsonify({
            'error': str(error),
            'type': 'ValidationError'
        }), 422
    
    @app.errorhandler(AuthenticationError)
    def handle_auth_error(error):
        """Handle authentication errors."""
        return jsonify({
            'error': str(error),
            'type': 'AuthenticationError'
        }), 401
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 errors."""
        return jsonify({
            'error': 'Resource not found',
            'type': 'NotFoundError'
        }), 404
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle internal server errors."""
        return jsonify({
            'error': 'Internal server error',
            'type': 'InternalError'
        }), 500


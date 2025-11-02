"""
API routes definition.
"""

from flask import Flask, jsonify, request
from typing import Dict, Any

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.
    
    Returns:
        dict: Health status
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Application is running'
    })


@app.route('/api/v1/info', methods=['GET'])
def get_info() -> Dict[str, Any]:
    """
    Get application information.
    
    Returns:
        dict: Application information
    """
    return jsonify({
        'name': 'FlowForge',
        'version': '1.0.0',
        'status': 'operational',
        'description': 'Modern CI/CD pipeline orchestration platform'
    })


def create_app(config_object=None):
    """
    Application factory pattern.
    
    Args:
        config_object: Configuration object
        
    Returns:
        Flask: Flask application instance
    """
    if config_object:
        app.config.from_object(config_object)
    
    return app


"""
Provider management API endpoints.

Allows adding, configuring, and managing CI/CD providers,
with secure token storage using keyring.
"""

from flask import Blueprint, jsonify, request
from typing import Dict, Any

from src.providers.registry import ProviderRegistry
from src.providers.base import ProviderConfig
from src.providers.github import GitHubProvider
from src.security.keyring_manager import KeyringManager
from src.api.pipelines import get_registry

providers_bp = Blueprint('providers', __name__, url_prefix='/api/v1/providers')


@providers_bp.route('', methods=['POST'])
def add_provider():
    """
    Add a new CI/CD provider.
    
    Request body:
    {
        "name": "github-main",
        "type": "github",
        "token": "ghp_...",
        "owner": "org",
        "repo": "repo",
        "enabled": true,
        "refresh_interval": 30
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'Request body required'}), 400
        
        name = data.get('name')
        provider_type = data.get('type')
        token = data.get('token')
        
        if not name or not provider_type:
            return jsonify({'error': 'name and type are required'}), 400
        
        registry = get_registry()
        
        # Check if provider already exists
        if registry.get(name):
            return jsonify({'error': f'Provider {name} already exists'}), 409
        
        # Store token securely in keyring
        if token:
            KeyringManager.set_token(provider_type, token)
        
        # Create provider config (without token in config dict)
        config_dict = {
            'owner': data.get('owner'),
            'repo': data.get('repo'),
            'base_url': data.get('base_url', 'https://api.github.com')
        }
        
        # Get token from keyring if not provided
        if not token:
            stored_token = KeyringManager.get_token(provider_type)
            if stored_token:
                config_dict['token'] = stored_token
        
        config = ProviderConfig(
            name=name,
            provider_type=provider_type,
            enabled=data.get('enabled', True),
            refresh_interval=data.get('refresh_interval', 30),
            config=config_dict
        )
        
        # Create provider instance based on type
        if provider_type == 'github':
            provider = GitHubProvider(config)
        else:
            return jsonify({'error': f'Unsupported provider type: {provider_type}'}), 400
        
        # Validate credentials
        if not provider.validate_credentials():
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Register provider
        registry.register(provider)
        
        return jsonify({
            'message': 'Provider added successfully',
            'provider': {
                'name': provider.name,
                'type': provider.provider_type,
                'enabled': provider.config.enabled
            }
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@providers_bp.route('', methods=['GET'])
def list_providers():
    """List all registered providers."""
    registry = get_registry()
    providers = registry.get_all()
    
    result = []
    for provider in providers:
        result.append({
            'name': provider.name,
            'type': provider.provider_type,
            'enabled': provider.config.enabled,
            'refresh_interval': provider.config.refresh_interval,
            'has_token': KeyringManager.has_token(provider.provider_type)
        })
    
    return jsonify({
        'providers': result,
        'count': len(result)
    }), 200


@providers_bp.route('/<provider_name>', methods=['DELETE'])
def remove_provider(provider_name: str):
    """Remove a provider."""
    registry = get_registry()
    provider = registry.get(provider_name)
    
    if not provider:
        return jsonify({'error': f'Provider {provider_name} not found'}), 404
    
    registry.unregister(provider_name)
    
    return jsonify({
        'message': f'Provider {provider_name} removed'
    }), 200


@providers_bp.route('/<provider_name>/token', methods=['PUT'])
def update_token(provider_name: str):
    """
    Update provider token securely.
    
    Request body:
    {
        "token": "new_token_here"
    }
    """
    try:
        provider = get_registry().get(provider_name)
        
        if not provider:
            return jsonify({'error': f'Provider {provider_name} not found'}), 404
        
        data = request.json
        if not data or 'token' not in data:
            return jsonify({'error': 'token is required'}), 400
        
        # Store token in keyring
        KeyringManager.set_token(provider.provider_type, data['token'])
        
        # Update provider config
        provider.token = data['token']
        provider.session.headers.update({
            'Authorization': f'token {data["token"]}'
        })
        
        # Validate new credentials
        if not provider.validate_credentials():
            return jsonify({'error': 'Invalid token'}), 401
        
        return jsonify({
            'message': 'Token updated successfully'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


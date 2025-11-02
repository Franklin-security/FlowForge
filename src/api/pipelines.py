"""
Pipeline management API endpoints.

Provides REST API for managing CI/CD pipelines across multiple providers,
inspired by pipedash's unified pipeline interface.
"""

from flask import Blueprint, jsonify, request
from typing import Dict, Any, List

from src.providers.registry import ProviderRegistry
from src.providers.base import Pipeline, PipelineRun
from src.database.db import get_db_manager

pipelines_bp = Blueprint('pipelines', __name__, url_prefix='/api/v1/pipelines')

# Global provider registry
_provider_registry = ProviderRegistry()


def get_registry() -> ProviderRegistry:
    """Get global provider registry."""
    return _provider_registry


@pipelines_bp.route('', methods=['GET'])
def list_pipelines():
    """
    List all pipelines from all enabled providers.
    
    Returns:
        JSON list of pipelines
    """
    try:
        pipelines = _provider_registry.fetch_all_pipelines()
        
        # Convert Pipeline objects to dictionaries
        result = []
        for pipeline in pipelines:
            result.append({
                'id': pipeline.id,
                'name': pipeline.name,
                'status': pipeline.status.value,
                'repository': pipeline.repository,
                'branch': pipeline.branch,
                'commit': pipeline.commit,
                'commit_message': pipeline.commit_message,
                'author': pipeline.author,
                'started_at': pipeline.started_at,
                'finished_at': pipeline.finished_at,
                'url': pipeline.url,
                'provider': pipeline.provider
            })
        
        return jsonify({
            'pipelines': result,
            'count': len(result)
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@pipelines_bp.route('/providers', methods=['GET'])
def list_providers():
    """
    List all registered providers.
    
    Returns:
        JSON list of provider information
    """
    providers = _provider_registry.get_all()
    
    result = []
    for provider in providers:
        result.append({
            'name': provider.name,
            'type': provider.provider_type,
            'enabled': provider.config.enabled,
            'refresh_interval': provider.config.refresh_interval
        })
    
    return jsonify({
        'providers': result,
        'count': len(result)
    }), 200


@pipelines_bp.route('/<provider_name>/pipelines', methods=['GET'])
def list_provider_pipelines(provider_name: str):
    """
    List pipelines for a specific provider.
    
    Args:
        provider_name: Name of the provider
        
    Returns:
        JSON list of pipelines from the provider
    """
    provider = _provider_registry.get(provider_name)
    
    if not provider:
        return jsonify({
            'error': f'Provider {provider_name} not found'
        }), 404
    
    try:
        pipelines = provider.fetch_pipelines()
        
        result = []
        for pipeline in pipelines:
            result.append({
                'id': pipeline.id,
                'name': pipeline.name,
                'status': pipeline.status.value,
                'repository': pipeline.repository,
                'branch': pipeline.branch,
                'commit': pipeline.commit,
                'url': pipeline.url
            })
        
        return jsonify({
            'pipelines': result,
            'provider': provider_name,
            'count': len(result)
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@pipelines_bp.route('/<provider_name>/pipelines/<pipeline_id>/trigger', methods=['POST'])
def trigger_pipeline(provider_name: str, pipeline_id: str):
    """
    Trigger a pipeline execution.
    
    Args:
        provider_name: Name of the provider
        pipeline_id: Pipeline identifier
        
    Returns:
        JSON object with run information
    """
    provider = _provider_registry.get(provider_name)
    
    if not provider:
        return jsonify({
            'error': f'Provider {provider_name} not found'
        }), 404
    
    try:
        parameters = request.json or {}
        run = provider.trigger_pipeline(pipeline_id, parameters)
        
        return jsonify({
            'run': {
                'id': run.id,
                'pipeline_id': run.pipeline_id,
                'status': run.status.value,
                'started_at': run.started_at
            }
        }), 201
    
    except NotImplementedError:
        return jsonify({
            'error': 'Pipeline triggering not implemented for this provider'
        }), 501
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@pipelines_bp.route('/<provider_name>/runs/<run_id>/cancel', methods=['POST'])
def cancel_run(provider_name: str, run_id: str):
    """
    Cancel a running pipeline.
    
    Args:
        provider_name: Name of the provider
        run_id: Run identifier
        
    Returns:
        JSON object with cancellation status
    """
    provider = _provider_registry.get(provider_name)
    
    if not provider:
        return jsonify({
            'error': f'Provider {provider_name} not found'
        }), 404
    
    try:
        success = provider.cancel_pipeline(run_id)
        
        return jsonify({
            'success': success,
            'run_id': run_id
        }), 200
    
    except NotImplementedError:
        return jsonify({
            'error': 'Pipeline cancellation not implemented for this provider'
        }), 501
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


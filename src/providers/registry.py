"""
Provider registry for managing CI/CD provider plugins.

The registry maintains a list of configured providers and provides
methods to interact with them collectively.
"""

from typing import List, Dict, Optional
from src.providers.base import BaseProvider, ProviderConfig, Pipeline


class ProviderRegistry:
    """
    Registry for managing CI/CD provider instances.
    
    Inspired by pipedash's plugin system, this class maintains
    a collection of provider instances and provides unified access.
    """
    
    def __init__(self):
        """Initialize empty registry."""
        self._providers: Dict[str, BaseProvider] = {}
    
    def register(self, provider: BaseProvider) -> None:
        """
        Register a provider instance.
        
        Args:
            provider: Provider instance to register
            
        Raises:
            ValueError: If provider name already exists
        """
        if provider.name in self._providers:
            raise ValueError(f"Provider '{provider.name}' already registered")
        
        self._providers[provider.name] = provider
    
    def unregister(self, name: str) -> None:
        """
        Unregister a provider.
        
        Args:
            name: Provider name to unregister
        """
        if name in self._providers:
            del self._providers[name]
    
    def get(self, name: str) -> Optional[BaseProvider]:
        """
        Get provider by name.
        
        Args:
            name: Provider name
            
        Returns:
            Provider instance or None if not found
        """
        return self._providers.get(name)
    
    def get_all(self) -> List[BaseProvider]:
        """
        Get all registered providers.
        
        Returns:
            List of all provider instances
        """
        return list(self._providers.values())
    
    def get_enabled(self) -> List[BaseProvider]:
        """
        Get all enabled providers.
        
        Returns:
            List of enabled provider instances
        """
        return [
            provider for provider in self._providers.values()
            if provider.config.enabled
        ]
    
    def get_by_type(self, provider_type: str) -> List[BaseProvider]:
        """
        Get providers by type.
        
        Args:
            provider_type: Provider type (github, gitlab, etc.)
            
        Returns:
            List of providers of specified type
        """
        return [
            provider for provider in self._providers.values()
            if provider.provider_type == provider_type
        ]
    
    def fetch_all_pipelines(self) -> List[Pipeline]:
        """
        Fetch pipelines from all enabled providers.
        
        Returns:
            List of all pipelines from all providers
        """
        all_pipelines = []
        
        for provider in self.get_enabled():
            try:
                pipelines = provider.fetch_pipelines()
                all_pipelines.extend(pipelines)
            except Exception as e:
                # Log error but continue with other providers
                print(f"Error fetching pipelines from {provider.name}: {e}")
                continue
        
        return all_pipelines
    
    def count(self) -> int:
        """
        Get total number of registered providers.
        
        Returns:
            Number of providers
        """
        return len(self._providers)
    
    def clear(self) -> None:
        """Clear all registered providers."""
        self._providers.clear()
    
    def __repr__(self) -> str:
        return f"ProviderRegistry(count={self.count()})"


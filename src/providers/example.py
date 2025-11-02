"""
Example usage of FlowForge provider system.

This module demonstrates how to use the provider architecture,
inspired by pipedash's plugin system.
"""

from src.providers.base import ProviderConfig
from src.providers.github import GitHubProvider
from src.providers.registry import ProviderRegistry


def example_setup():
    """
    Example: Setting up a GitHub provider.
    
    This demonstrates how to configure and register a provider,
    similar to how pipedash manages provider instances.
    """
    # Create provider registry
    registry = ProviderRegistry()
    
    # Configure GitHub provider
    github_config = ProviderConfig(
        name='github-main',
        provider_type='github',
        enabled=True,
        refresh_interval=30,
        config={
            'token': 'your-github-token-here',
            'owner': 'your-org',
            'repo': 'your-repo',
            'base_url': 'https://api.github.com'  # Optional, for GitHub Enterprise
        }
    )
    
    # Create and register provider
    github_provider = GitHubProvider(github_config)
    
    # Validate credentials
    if github_provider.validate_credentials():
        print("✓ GitHub credentials valid")
        registry.register(github_provider)
    else:
        print("✗ GitHub credentials invalid")
    
    # Fetch pipelines from all providers
    pipelines = registry.fetch_all_pipelines()
    
    print(f"Found {len(pipelines)} pipelines")
    for pipeline in pipelines:
        print(f"  - {pipeline.name}: {pipeline.status.value}")
    
    return registry


if __name__ == '__main__':
    example_setup()


#!/usr/bin/env python3
"""
Basic usage example for FlowForge.

Demonstrates how to use FlowForge to manage CI/CD pipelines.
"""

from src.providers.base import ProviderConfig
from src.providers.github import GitHubProvider
from src.providers.registry import ProviderRegistry
from src.security.keyring_manager import KeyringManager
from src.workers import PipelinePoller
import time


def main():
    """Basic usage example."""
    print("=" * 60)
    print("FlowForge - Basic Usage Example")
    print("=" * 60)
    print()
    
    # Step 1: Store token securely
    print("Step 1: Storing GitHub token securely...")
    token = input("Enter your GitHub token (or press Enter to skip): ").strip()
    
    if token:
        KeyringManager.set_token('github', token)
        print("✓ Token stored securely in keyring")
    else:
        print("⚠ Using existing token from keyring (if available)")
    
    print()
    
    # Step 2: Configure provider
    print("Step 2: Configuring GitHub provider...")
    owner = input("GitHub owner/organization: ").strip() or "octocat"
    repo = input("Repository name: ").strip() or "Hello-World"
    
    config = ProviderConfig(
        name='github-example',
        provider_type='github',
        enabled=True,
        refresh_interval=30,
        config={
            'owner': owner,
            'repo': repo,
            'base_url': 'https://api.github.com'
        }
    )
    
    # Get token from keyring if not provided
    if not token:
        stored_token = KeyringManager.get_token('github')
        if stored_token:
            config.config['token'] = stored_token
        else:
            print("❌ No token found. Please run again and provide a token.")
            return
    
    print()
    
    # Step 3: Create and register provider
    print("Step 3: Creating provider...")
    provider = GitHubProvider(config)
    
    if not provider.validate_credentials():
        print("❌ Invalid credentials. Please check your token.")
        return
    
    print("✓ Credentials validated")
    
    registry = ProviderRegistry()
    registry.register(provider)
    print(f"✓ Provider '{provider.name}' registered")
    print()
    
    # Step 4: Fetch pipelines
    print("Step 4: Fetching pipelines...")
    pipelines = provider.fetch_pipelines()
    
    if not pipelines:
        print("⚠ No pipelines found")
        return
    
    print(f"✓ Found {len(pipelines)} pipeline(s)")
    print()
    
    # Display pipelines
    print("Pipelines:")
    for pipeline in pipelines:
        status_icon = {
            'success': '✓',
            'failure': '✗',
            'running': '⟳',
            'pending': '○',
            'cancelled': '⊘'
        }.get(pipeline.status.value, '?')
        
        print(f"  {status_icon} {pipeline.name} ({pipeline.status.value})")
        print(f"    Repository: {pipeline.repository}")
        print(f"    Branch: {pipeline.branch}")
        if pipeline.commit:
            print(f"    Commit: {pipeline.commit[:8]}")
        print()
    
    # Step 5: Optional - Start background polling
    print("Step 5: Background polling (optional)")
    start_poller = input("Start background poller? (y/N): ").strip().lower()
    
    if start_poller == 'y':
        poller = PipelinePoller(registry, interval=30)
        poller.start()
        print("✓ Background poller started")
        print("  Press Ctrl+C to stop...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            poller.stop()
            print("\n✓ Background poller stopped")
    
    print()
    print("=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()


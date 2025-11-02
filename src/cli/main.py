"""
Main CLI interface using Click and Rich.

Provides beautiful command-line interface for FlowForge operations.
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.utils.logger import get_logger
from src.providers.registry import ProviderRegistry
from src.providers.base import ProviderConfig
from src.providers.github import GitHubProvider
from src.security.keyring_manager import KeyringManager
from src.api.pipelines import get_registry

console = Console()
logger = get_logger(__name__)


@click.group()
@click.version_option(version='1.0.0', prog_name='flowforge')
def cli():
    """
    FlowForge - CI/CD Pipeline Orchestration Platform
    
    Manage CI/CD pipelines from multiple providers through a unified interface.
    """
    pass


@cli.command()
def status():
    """Show FlowForge status and registered providers."""
    registry = get_registry()
    providers = registry.get_all()
    
    console.print("\n[bold cyan]FlowForge Status[/bold cyan]\n")
    
    if not providers:
        console.print("[yellow]No providers registered[/yellow]")
        console.print("\nUse [bold]flowforge provider add[/bold] to add a provider\n")
        return
    
    # Create status table
    table = Table(title="Registered Providers")
    table.add_column("Name", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Status", justify="center")
    table.add_column("Refresh", style="yellow")
    table.add_column("Token", justify="center")
    
    for provider in providers:
        status_icon = "✓" if provider.config.enabled else "✗"
        status_color = "green" if provider.config.enabled else "red"
        has_token = KeyringManager.has_token(provider.provider_type)
        token_icon = "✓" if has_token else "✗"
        
        table.add_row(
            provider.name,
            provider.provider_type,
            f"[{status_color}]{status_icon}[/{status_color}]",
            f"{provider.config.refresh_interval}s",
            "[green]✓" if has_token else "[red]✗"
        )
    
    console.print(table)
    console.print(f"\n[dim]Total providers: {len(providers)}[/dim]\n")


@cli.group()
def provider():
    """Manage CI/CD providers."""
    pass


@provider.command('add')
@click.option('--name', prompt='Provider name', help='Unique name for this provider')
@click.option('--type', 'provider_type', type=click.Choice(['github'], case_sensitive=False),
              prompt='Provider type', help='Type of CI/CD provider')
@click.option('--token', prompt=True, hide_input=True, help='API token')
@click.option('--owner', prompt='Owner/Organization', help='GitHub owner or organization')
@click.option('--repo', prompt='Repository', help='Repository name')
@click.option('--enabled/--disabled', default=True, help='Enable this provider')
@click.option('--refresh-interval', default=30, type=int, help='Polling interval in seconds')
def add_provider(name, provider_type, token, owner, repo, enabled, refresh_interval):
    """Add a new CI/CD provider."""
    with console.status("[bold green]Adding provider..."):
        # Store token securely
        KeyringManager.set_token(provider_type, token)
        
        # Create provider config
        config = ProviderConfig(
            name=name,
            provider_type=provider_type.lower(),
            enabled=enabled,
            refresh_interval=refresh_interval,
            config={
                'owner': owner,
                'repo': repo,
                'base_url': 'https://api.github.com'
            }
        )
        
        # Create provider instance
        if provider_type.lower() == 'github':
            provider = GitHubProvider(config)
        else:
            console.print(f"[red]Unsupported provider type: {provider_type}[/red]")
            return
        
        # Validate credentials
        if not provider.validate_credentials():
            console.print("[red]✗ Invalid credentials[/red]")
            return
        
        # Register provider
        registry = get_registry()
        try:
            registry.register(provider)
            console.print(f"[green]✓ Provider '{name}' added successfully[/green]")
        except ValueError as e:
            console.print(f"[red]✗ Error: {e}[/red]")


@provider.command('list')
def list_providers():
    """List all registered providers."""
    registry = get_registry()
    providers = registry.get_all()
    
    if not providers:
        console.print("[yellow]No providers registered[/yellow]\n")
        return
    
    table = Table(title="Registered Providers")
    table.add_column("Name", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Repository", style="yellow")
    table.add_column("Enabled", justify="center")
    
    for provider in providers:
        repo = f"{provider.config.config.get('owner', '')}/{provider.config.config.get('repo', '')}"
        enabled = "✓" if provider.config.enabled else "✗"
        
        table.add_row(
            provider.name,
            provider.provider_type,
            repo,
            enabled
        )
    
    console.print(table)
    console.print()


@provider.command('remove')
@click.argument('name')
def remove_provider(name):
    """Remove a provider."""
    registry = get_registry()
    provider = registry.get(name)
    
    if not provider:
        console.print(f"[red]Provider '{name}' not found[/red]\n")
        return
    
    registry.unregister(name)
    console.print(f"[green]✓ Provider '{name}' removed[/green]\n")


@cli.group()
def pipeline():
    """Manage CI/CD pipelines."""
    pass


@pipeline.command('list')
@click.option('--provider', help='Filter by provider name')
def list_pipelines(provider):
    """List all pipelines."""
    registry = get_registry()
    
    if provider:
        provider_instance = registry.get(provider)
        if not provider_instance:
            console.print(f"[red]Provider '{provider}' not found[/red]\n")
            return
        pipelines = provider_instance.fetch_pipelines()
    else:
        pipelines = registry.fetch_all_pipelines()
    
    if not pipelines:
        console.print("[yellow]No pipelines found[/yellow]\n")
        return
    
    table = Table(title="Pipelines")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Status", justify="center")
    table.add_column("Repository", style="yellow")
    table.add_column("Branch", style="blue")
    
    for pipeline in pipelines:
        status_colors = {
            'success': 'green',
            'failure': 'red',
            'running': 'yellow',
            'pending': 'blue',
            'cancelled': 'dim'
        }
        status_color = status_colors.get(pipeline.status.value, 'white')
        status_text = f"[{status_color}]{pipeline.status.value.upper()}[/{status_color}]"
        
        table.add_row(
            pipeline.id[:8],
            pipeline.name,
            status_text,
            pipeline.repository,
            pipeline.branch
        )
    
    console.print(table)
    console.print()


@pipeline.command('trigger')
@click.argument('provider_name')
@click.argument('pipeline_id')
@click.option('--ref', default='main', help='Branch or tag')
@click.option('--inputs', help='JSON string of workflow inputs')
def trigger_pipeline(provider_name, pipeline_id, ref, inputs):
    """Trigger a pipeline."""
    import json
    
    registry = get_registry()
    provider = registry.get(provider_name)
    
    if not provider:
        console.print(f"[red]Provider '{provider_name}' not found[/red]\n")
        return
    
    try:
        parameters = {'ref': ref}
        if inputs:
            parameters['inputs'] = json.loads(inputs)
        
        with console.status(f"[bold green]Triggering pipeline {pipeline_id}..."):
            run = provider.trigger_pipeline(pipeline_id, parameters)
            console.print(f"[green]✓ Pipeline triggered successfully[/green]")
            console.print(f"Run ID: {run.id}")
            console.print(f"Status: {run.status.value}\n")
    
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]\n")


@cli.command()
def serve():
    """Start FlowForge API server."""
    from src.main import main
    main()


if __name__ == '__main__':
    cli()


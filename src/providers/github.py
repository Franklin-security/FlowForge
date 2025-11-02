"""
GitHub Actions provider implementation.

This module implements the GitHub Actions provider plugin.
"""

import requests
from typing import List, Dict, Any
from src.providers.base import (
    BaseProvider,
    ProviderConfig,
    Pipeline,
    PipelineRun,
    PipelineStatus
)


class GitHubProvider(BaseProvider):
    """
    GitHub Actions provider implementation.
    
    Supports:
    - Fetching workflows and runs
    - Triggering workflows via workflow_dispatch
    - Re-running failed workflows
    - Cancelling running workflows
    """
    
    def __init__(self, config: ProviderConfig):
        """
        Initialize GitHub provider.
        
        Args:
            config: Provider configuration with GitHub token and repo info
        """
        super().__init__(config)
        self.token = config.config.get('token')
        self.owner = config.config.get('owner')
        self.repo = config.config.get('repo')
        self.base_url = config.config.get('base_url', 'https://api.github.com')
        
        self.session = requests.Session()
        if self.token:
            self.session.headers.update({
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            })
    
    def validate_credentials(self) -> bool:
        """
        Validate GitHub credentials.
        
        Returns:
            bool: True if credentials are valid
        """
        if not self.token:
            return False
        
        try:
            response = self.session.get(f'{self.base_url}/user')
            return response.status_code == 200
        except Exception:
            return False
    
    def fetch_pipelines(self) -> List[Pipeline]:
        """
        Fetch GitHub Actions workflows.
        
        Returns:
            List of Pipeline objects representing workflows
        """
        if not self.owner or not self.repo:
            return []
        
        pipelines = []
        
        try:
            # Fetch workflows
            url = f'{self.base_url}/repos/{self.owner}/{self.repo}/actions/workflows'
            response = self.session.get(url)
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            
            for workflow in data.get('workflows', []):
                # Get latest run for status
                runs_url = f'{self.base_url}/repos/{self.owner}/{self.repo}/actions/workflows/{workflow["id"]}/runs'
                runs_response = self.session.get(runs_url, params={'per_page': 1})
                
                latest_run = None
                if runs_response.status_code == 200:
                    runs_data = runs_response.json()
                    if runs_data.get('workflow_runs'):
                        latest_run = runs_data['workflow_runs'][0]
                
                # Determine status
                if latest_run:
                    status_str = latest_run.get('status', 'unknown')
                    conclusion = latest_run.get('conclusion')
                    
                    if status_str == 'in_progress' or status_str == 'queued':
                        status = PipelineStatus.RUNNING
                    elif conclusion == 'success':
                        status = PipelineStatus.SUCCESS
                    elif conclusion == 'failure':
                        status = PipelineStatus.FAILURE
                    elif conclusion == 'cancelled':
                        status = PipelineStatus.CANCELLED
                    else:
                        status = PipelineStatus.PENDING
                else:
                    status = PipelineStatus.PENDING
                
                pipeline = Pipeline(
                    id=str(workflow['id']),
                    name=workflow['name'],
                    status=status,
                    repository=f"{self.owner}/{self.repo}",
                    branch=latest_run.get('head_branch', 'unknown') if latest_run else 'unknown',
                    commit=latest_run.get('head_sha', '') if latest_run else '',
                    commit_message=latest_run.get('head_commit', {}).get('message', '') if latest_run else '',
                    author=latest_run.get('head_commit', {}).get('author', {}).get('name', '') if latest_run else '',
                    started_at=latest_run.get('created_at') if latest_run else None,
                    finished_at=latest_run.get('updated_at') if latest_run and latest_run.get('status') == 'completed' else None,
                    url=workflow.get('html_url', ''),
                    provider=self.name
                )
                pipelines.append(pipeline)
        
        except Exception as e:
            print(f"Error fetching GitHub pipelines: {e}")
        
        return pipelines
    
    def fetch_pipeline_runs(self, pipeline_id: str, limit: int = 10) -> List[PipelineRun]:
        """Fetch workflow run history."""
        # Implementation placeholder
        return []
    
    def trigger_pipeline(self, pipeline_id: str, parameters: Dict[str, Any] = None) -> PipelineRun:
        """Trigger a workflow via workflow_dispatch."""
        # Implementation placeholder
        raise NotImplementedError("GitHub workflow triggering not yet implemented")
    
    def re_run_pipeline(self, run_id: str) -> PipelineRun:
        """Re-run a workflow."""
        # Implementation placeholder
        raise NotImplementedError("GitHub workflow re-run not yet implemented")
    
    def cancel_pipeline(self, run_id: str) -> bool:
        """Cancel a running workflow."""
        # Implementation placeholder
        raise NotImplementedError("GitHub workflow cancellation not yet implemented")
    
    def get_pipeline_status(self, pipeline_id: str) -> PipelineStatus:
        """Get current workflow status."""
        pipelines = self.fetch_pipelines()
        for pipeline in pipelines:
            if pipeline.id == pipeline_id:
                return pipeline.status
        return PipelineStatus.ERROR
    
    def get_available_parameters(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow inputs for workflow_dispatch."""
        # Implementation placeholder
        return {}


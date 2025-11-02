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
        """
        Fetch workflow run history.
        
        Args:
            pipeline_id: Workflow ID
            limit: Maximum number of runs to fetch
            
        Returns:
            List of PipelineRun objects
        """
        if not self.owner or not self.repo:
            return []
        
        runs = []
        
        try:
            url = f'{self.base_url}/repos/{self.owner}/{self.repo}/actions/workflows/{pipeline_id}/runs'
            response = self.session.get(url, params={'per_page': limit})
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            
            for run_data in data.get('workflow_runs', []):
                # Calculate duration
                duration = None
                if run_data.get('created_at') and run_data.get('updated_at'):
                    from datetime import datetime
                    started = datetime.fromisoformat(run_data['created_at'].replace('Z', '+00:00'))
                    finished = datetime.fromisoformat(run_data['updated_at'].replace('Z', '+00:00'))
                    if run_data.get('status') == 'completed':
                        duration = (finished - started).total_seconds()
                
                # Map status
                status_str = run_data.get('status', 'unknown')
                conclusion = run_data.get('conclusion')
                
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
                
                run = PipelineRun(
                    id=str(run_data['id']),
                    pipeline_id=pipeline_id,
                    status=status,
                    started_at=run_data.get('created_at'),
                    finished_at=run_data.get('updated_at') if run_data.get('status') == 'completed' else None,
                    duration=duration
                )
                runs.append(run)
        
        except Exception as e:
            print(f"Error fetching pipeline runs: {e}")
        
        return runs
    
    def trigger_pipeline(self, pipeline_id: str, parameters: Dict[str, Any] = None) -> PipelineRun:
        """
        Trigger a workflow via workflow_dispatch.
        
        Args:
            pipeline_id: Workflow ID to trigger
            parameters: Input parameters (inputs) for the workflow
            
        Returns:
            PipelineRun object for the triggered run
        """
        if not self.owner or not self.repo:
            raise ValueError("Owner and repo must be set")
        
        try:
            # Get workflow file path (needed for dispatch)
            workflow_url = f'{self.base_url}/repos/{self.owner}/{self.repo}/actions/workflows/{pipeline_id}'
            workflow_response = self.session.get(workflow_url)
            
            if workflow_response.status_code != 200:
                raise Exception(f"Workflow not found: {workflow_response.status_code}")
            
            workflow_data = workflow_response.json()
            workflow_path = workflow_data['path']
            
            # Trigger workflow dispatch
            dispatch_url = f'{self.base_url}/repos/{self.owner}/{self.repo}/actions/workflows/{workflow_path}/dispatches'
            
            payload = {
                'ref': parameters.get('ref', 'main') if parameters else 'main'
            }
            
            # Add inputs if provided
            if parameters and 'inputs' in parameters:
                payload['inputs'] = parameters['inputs']
            
            response = self.session.post(dispatch_url, json=payload)
            
            if response.status_code == 204:
                # Successfully triggered, fetch the new run
                # Note: We need to poll for the new run as GitHub doesn't return it immediately
                import time
                time.sleep(2)  # Wait a bit for the run to be created
                
                runs = self.fetch_pipeline_runs(pipeline_id, limit=1)
                if runs:
                    return runs[0]
                
                # If we can't find the run, return a pending run object
                return PipelineRun(
                    id=f"pending_{pipeline_id}",
                    pipeline_id=pipeline_id,
                    status=PipelineStatus.PENDING,
                    parameters=parameters
                )
            else:
                raise Exception(f"Failed to trigger workflow: {response.status_code} - {response.text}")
        
        except Exception as e:
            print(f"Error triggering pipeline: {e}")
            raise
    
    def re_run_pipeline(self, run_id: str) -> PipelineRun:
        """
        Re-run a failed workflow run.
        
        Args:
            run_id: Run ID to re-run
            
        Returns:
            PipelineRun object for the new run
        """
        if not self.owner or not self.repo:
            raise ValueError("Owner and repo must be set")
        
        try:
            url = f'{self.base_url}/repos/{self.owner}/{self.repo}/actions/runs/{run_id}/rerun'
            response = self.session.post(url)
            
            if response.status_code == 201:
                # Get the workflow ID first
                run_info_url = f'{self.base_url}/repos/{self.owner}/{self.repo}/actions/runs/{run_id}'
                run_info = self.session.get(run_info_url)
                
                if run_info.status_code == 200:
                    workflow_id = run_info.json()['workflow_id']
                    
                    # Fetch the new run
                    import time
                    time.sleep(2)
                    runs = self.fetch_pipeline_runs(str(workflow_id), limit=10)
                    
                    # Find the most recent run (should be the re-run)
                    if runs:
                        return runs[0]
                
                return PipelineRun(
                    id=f"rerun_{run_id}",
                    pipeline_id="unknown",
                    status=PipelineStatus.PENDING
                )
            else:
                raise Exception(f"Failed to re-run: {response.status_code} - {response.text}")
        
        except Exception as e:
            print(f"Error re-running pipeline: {e}")
            raise
    
    def cancel_pipeline(self, run_id: str) -> bool:
        """
        Cancel a running workflow.
        
        Args:
            run_id: Run ID to cancel
            
        Returns:
            bool: True if cancellation was successful
        """
        if not self.owner or not self.repo:
            return False
        
        try:
            url = f'{self.base_url}/repos/{self.owner}/{self.repo}/actions/runs/{run_id}/cancel'
            response = self.session.post(url)
            
            return response.status_code == 202
        
        except Exception as e:
            print(f"Error cancelling pipeline: {e}")
            return False
    
    def get_pipeline_status(self, pipeline_id: str) -> PipelineStatus:
        """Get current workflow status."""
        pipelines = self.fetch_pipelines()
        for pipeline in pipelines:
            if pipeline.id == pipeline_id:
                return pipeline.status
        return PipelineStatus.ERROR
    
    def get_available_parameters(self, workflow_id: str) -> Dict[str, Any]:
        """
        Get workflow inputs for workflow_dispatch.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Dictionary of available input parameters
        """
        if not self.owner or not self.repo:
            return {}
        
        try:
            # Get workflow definition
            url = f'{self.base_url}/repos/{self.owner}/{self.repo}/actions/workflows/{workflow_id}'
            response = self.session.get(url)
            
            if response.status_code != 200:
                return {}
            
            workflow_data = response.json()
            workflow_path = workflow_data.get('path')
            
            # Get workflow file content to parse inputs
            # Note: This requires additional GitHub API call or parsing YAML
            # For now, return basic structure
            return {
                'ref': {
                    'type': 'string',
                    'description': 'Branch or tag to run workflow on',
                    'default': 'main'
                },
                'inputs': {
                    'description': 'Workflow inputs (requires parsing workflow file)',
                    'type': 'object'
                }
            }
        
        except Exception as e:
            print(f"Error getting workflow parameters: {e}")
            return {}


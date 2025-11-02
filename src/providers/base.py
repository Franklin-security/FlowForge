"""
Base provider interface for CI/CD providers.

Inspired by pipedash plugin architecture, this module defines the common
interface that all CI/CD providers must implement.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class PipelineStatus(Enum):
    """Pipeline execution status."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    CANCELLED = "cancelled"
    ERROR = "error"


@dataclass
class ProviderConfig:
    """
    Configuration for a CI/CD provider instance.
    
    Attributes:
        name: Unique name for this provider instance
        provider_type: Type of provider (github, gitlab, jenkins, etc.)
        enabled: Whether this provider is enabled
        refresh_interval: Polling interval in seconds
        config: Provider-specific configuration dictionary
    """
    name: str
    provider_type: str
    enabled: bool = True
    refresh_interval: int = 30
    config: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.config is None:
            self.config = {}


@dataclass
class Pipeline:
    """
    Represents a CI/CD pipeline.
    
    Attributes:
        id: Unique pipeline identifier
        name: Pipeline/workflow name
        status: Current status
        repository: Repository name/organization
        branch: Branch name
        commit: Commit SHA
        commit_message: Commit message
        author: Commit author
        started_at: Start timestamp
        finished_at: Finish timestamp (if completed)
        url: Link to pipeline in provider's UI
        provider: Provider name
    """
    id: str
    name: str
    status: PipelineStatus
    repository: str
    branch: str
    commit: str
    commit_message: Optional[str] = None
    author: Optional[str] = None
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    url: Optional[str] = None
    provider: Optional[str] = None


@dataclass
class PipelineRun:
    """
    Represents a single pipeline execution/run.
    
    Attributes:
        id: Unique run identifier
        pipeline_id: Parent pipeline ID
        status: Run status
        started_at: Start timestamp
        finished_at: Finish timestamp
        duration: Duration in seconds
        parameters: Input parameters used for this run
    """
    id: str
    pipeline_id: str
    status: PipelineStatus
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    duration: Optional[float] = None
    parameters: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}


class BaseProvider(ABC):
    """
    Abstract base class for CI/CD provider plugins.
    
    All provider implementations must inherit from this class and
    implement the abstract methods. This follows the plugin architecture
    pattern from pipedash.
    """
    
    def __init__(self, config: ProviderConfig):
        """
        Initialize provider with configuration.
        
        Args:
            config: Provider configuration
        """
        self.config = config
        self.name = config.name
        self.provider_type = config.provider_type
    
    @abstractmethod
    def validate_credentials(self) -> bool:
        """
        Validate provider credentials.
        
        Returns:
            bool: True if credentials are valid
        """
        pass
    
    @abstractmethod
    def fetch_pipelines(self) -> List[Pipeline]:
        """
        Fetch all pipelines from the provider.
        
        Returns:
            List of Pipeline objects
        """
        pass
    
    @abstractmethod
    def fetch_pipeline_runs(self, pipeline_id: str, limit: int = 10) -> List[PipelineRun]:
        """
        Fetch run history for a pipeline.
        
        Args:
            pipeline_id: Pipeline identifier
            limit: Maximum number of runs to fetch
            
        Returns:
            List of PipelineRun objects
        """
        pass
    
    @abstractmethod
    def trigger_pipeline(self, pipeline_id: str, parameters: Dict[str, Any] = None) -> PipelineRun:
        """
        Trigger a pipeline execution.
        
        Args:
            pipeline_id: Pipeline to trigger
            parameters: Input parameters for the pipeline
            
        Returns:
            PipelineRun object for the triggered run
        """
        pass
    
    @abstractmethod
    def re_run_pipeline(self, run_id: str) -> PipelineRun:
        """
        Re-run a previous pipeline execution.
        
        Args:
            run_id: Run identifier to re-run
            
        Returns:
            PipelineRun object for the new run
        """
        pass
    
    @abstractmethod
    def cancel_pipeline(self, run_id: str) -> bool:
        """
        Cancel a running pipeline.
        
        Args:
            run_id: Run identifier to cancel
            
        Returns:
            bool: True if cancellation was successful
        """
        pass
    
    @abstractmethod
    def get_pipeline_status(self, pipeline_id: str) -> PipelineStatus:
        """
        Get current status of a pipeline.
        
        Args:
            pipeline_id: Pipeline identifier
            
        Returns:
            PipelineStatus enum value
        """
        pass
    
    def get_available_parameters(self, pipeline_id: str) -> Dict[str, Any]:
        """
        Get available input parameters for a pipeline.
        
        This is an optional method that providers can override.
        Default implementation returns empty dict.
        
        Args:
            pipeline_id: Pipeline identifier
            
        Returns:
            Dictionary of parameter definitions
        """
        return {}
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, type={self.provider_type})"


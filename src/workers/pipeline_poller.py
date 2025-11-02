"""
Pipeline poller for background updates.

Polls providers at configured intervals and updates cache,
inspired by pipedash's background refresh mechanism.
"""

import time
import threading
import logging
from typing import List, Optional
from datetime import datetime

from src.providers.registry import ProviderRegistry
from src.providers.base import BaseProvider
from src.database.db import get_db_manager
from src.database.models import PipelineModel, PipelineRunModel

logger = logging.getLogger(__name__)


class PipelinePoller:
    """
    Background worker for polling providers and updating cache.
    
    Runs in a separate thread and periodically fetches pipeline data
    from all enabled providers, updating the local cache.
    """
    
    def __init__(self, registry: ProviderRegistry, interval: int = 30):
        """
        Initialize pipeline poller.
        
        Args:
            registry: Provider registry
            interval: Default polling interval in seconds
        """
        self.registry = registry
        self.default_interval = interval
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.db = get_db_manager()
    
    def start(self) -> None:
        """Start the polling loop in background thread."""
        if self.running:
            logger.warning("Poller already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.thread.start()
        logger.info("Pipeline poller started")
    
    def stop(self) -> None:
        """Stop the polling loop."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Pipeline poller stopped")
    
    def _poll_loop(self) -> None:
        """Main polling loop."""
        while self.running:
            try:
                self._update_cache()
                
                # Wait for next poll (use shortest interval among providers)
                providers = self.registry.get_enabled()
                if providers:
                    min_interval = min(
                        p.config.refresh_interval for p in providers
                    ) or self.default_interval
                else:
                    min_interval = self.default_interval
                
                time.sleep(min_interval)
            
            except Exception as e:
                logger.error(f"Error in polling loop: {e}")
                time.sleep(self.default_interval)
    
    def _update_cache(self) -> None:
        """
        Update cache with latest pipeline data from all providers.
        
        Fetches pipelines from all enabled providers and updates
        the database cache.
        """
        providers = self.registry.get_enabled()
        
        if not providers:
            return
        
        logger.debug(f"Updating cache from {len(providers)} providers")
        
        with self.db.get_session() as session:
            for provider in providers:
                try:
                    pipelines = provider.fetch_pipelines()
                    self._save_pipelines(session, provider, pipelines)
                except Exception as e:
                    logger.error(f"Error fetching from {provider.name}: {e}")
                    continue
    
    def _save_pipelines(self, session, provider: BaseProvider, pipelines: List) -> None:
        """
        Save pipelines to database cache.
        
        Args:
            session: Database session
            provider: Provider instance
            pipelines: List of Pipeline objects
        """
        for pipeline in pipelines:
            try:
                # Check if pipeline exists
                existing = session.query(PipelineModel).filter_by(
                    id=pipeline.id
                ).first()
                
                if existing:
                    # Update existing
                    existing.status = pipeline.status.value
                    existing.branch = pipeline.branch
                    existing.commit = pipeline.commit
                    existing.commit_message = pipeline.commit_message
                    existing.author = pipeline.author
                    existing.started_at = datetime.fromisoformat(pipeline.started_at.replace('Z', '+00:00')) if pipeline.started_at else None
                    existing.finished_at = datetime.fromisoformat(pipeline.finished_at.replace('Z', '+00:00')) if pipeline.finished_at else None
                    existing.updated_at = datetime.utcnow()
                else:
                    # Create new
                    pipeline_model = PipelineModel(
                        id=pipeline.id,
                        name=pipeline.name,
                        status=pipeline.status.value,
                        repository=pipeline.repository,
                        branch=pipeline.branch,
                        commit=pipeline.commit,
                        commit_message=pipeline.commit_message,
                        author=pipeline.author,
                        url=pipeline.url,
                        started_at=datetime.fromisoformat(pipeline.started_at.replace('Z', '+00:00')) if pipeline.started_at else None,
                        finished_at=datetime.fromisoformat(pipeline.finished_at.replace('Z', '+00:00')) if pipeline.finished_at else None
                    )
                    session.add(pipeline_model)
            
            except Exception as e:
                logger.error(f"Error saving pipeline {pipeline.id}: {e}")
                continue
        
        session.commit()


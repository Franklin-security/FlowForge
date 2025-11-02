"""
Database module for FlowForge.

Provides SQLite database for caching pipeline data, inspired by pipedash's
data persistence layer.
"""

from src.database.models import Base, ProviderModel, PipelineModel, PipelineRunModel
from src.database.db import DatabaseManager

__all__ = ['Base', 'ProviderModel', 'PipelineModel', 'PipelineRunModel', 'DatabaseManager']


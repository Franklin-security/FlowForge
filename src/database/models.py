"""
Database models for FlowForge.

Defines SQLAlchemy models for storing pipeline and run data.
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PipelineModel(Base):
    """
    Database model for CI/CD pipelines.
    
    Caches pipeline information locally, similar to pipedash's
    pipeline data storage.
    """
    __tablename__ = 'pipelines'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    repository = Column(String, nullable=False)
    branch = Column(String)
    commit = Column(String)
    commit_message = Column(Text)
    author = Column(String)
    provider = Column(String, nullable=False)
    url = Column(String)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PipelineRunModel(Base):
    """
    Database model for pipeline runs/executions.
    
    Stores run history and metadata for pipeline executions.
    """
    __tablename__ = 'pipeline_runs'
    
    id = Column(String, primary_key=True)
    pipeline_id = Column(String, nullable=False)
    status = Column(String, nullable=False)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)
    duration = Column(Float)
    parameters = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


"""
Database models for FlowForge.

Defines SQLAlchemy models for storing pipeline and run data.
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class ProviderModel(Base):
    """
    Database model for CI/CD providers.
    
    Stores provider configuration and metadata.
    """
    __tablename__ = 'providers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    provider_type = Column(String, nullable=False)  # github, gitlab, jenkins
    enabled = Column(Boolean, default=True)
    refresh_interval = Column(Integer, default=30)  # seconds
    config = Column(JSON)  # Provider-specific configuration (without secrets)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    pipelines = relationship("PipelineModel", back_populates="provider")


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
    provider_id = Column(Integer, ForeignKey('providers.id'))
    provider = relationship("ProviderModel", back_populates="pipelines")
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
    commit_sha = Column(String)
    commit_message = Column(Text)
    author = Column(String)
    url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


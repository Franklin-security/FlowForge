"""
Database manager for FlowForge.

Manages SQLite database connection and operations for caching
pipeline data locally.
"""

import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.config import config
from src.database.models import Base


class DatabaseManager:
    """
    Database manager for SQLite operations.
    
    Provides connection management and session handling for
    pipeline data caching, similar to pipedash's SQLite usage.
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file.
                    Defaults to flowforge.db in current directory.
        """
        if db_path is None:
            db_path = Path.cwd() / 'flowforge.db'
        
        self.db_path = Path(db_path)
        self.engine = create_engine(
            f'sqlite:///{self.db_path}',
            connect_args={'check_same_thread': False},
            echo=False
        )
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def init_db(self) -> None:
        """
        Initialize database schema.
        
        Creates all tables defined in models.
        """
        Base.metadata.create_all(self.engine)
    
    @contextmanager
    def get_session(self):
        """
        Get database session context manager.
        
        Usage:
            with db.get_session() as session:
                # Use session
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_session(self) -> Session:
        """
        Get database session.
        
        Returns:
            SQLAlchemy session
            
        Note: Caller is responsible for closing the session
        """
        return self.SessionLocal()
    
    def close(self) -> None:
        """Close database connection."""
        self.engine.dispose()


# Global database instance
_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """
    Get global database manager instance.
    
    Returns:
        DatabaseManager instance
    """
    global _db_manager
    
    if _db_manager is None:
        db_path = config.DATABASE_URL or None
        _db_manager = DatabaseManager(db_path)
        _db_manager.init_db()
    
    return _db_manager


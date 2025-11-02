"""
Application configuration module.
"""

import os
from typing import Optional


class Config:
    """
    Application configuration class.
    Loads configuration from environment variables with sensible defaults.
    """
    
    # Application settings
    APP_NAME: str = os.getenv('APP_NAME', 'FlowForge')
    APP_VERSION: str = os.getenv('APP_VERSION', '1.0.0')
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Server settings
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '8000'))
    
    # Database settings (if needed)
    DATABASE_URL: Optional[str] = os.getenv('DATABASE_URL')
    
    # GitHub settings
    GITHUB_TOKEN: Optional[str] = os.getenv('GITHUB_TOKEN')
    GITHUB_REPO: Optional[str] = os.getenv('GITHUB_REPO')
    
    # API settings
    API_KEY: Optional[str] = os.getenv('API_KEY')
    API_SECRET: Optional[str] = os.getenv('API_SECRET')
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate configuration values.
        
        Returns:
            bool: True if configuration is valid
        """
        # Add validation logic here
        return True


# Create global config instance
config = Config()


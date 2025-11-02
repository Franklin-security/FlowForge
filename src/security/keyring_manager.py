"""
Keyring manager for secure secret storage.

Implements secure token storage using system keyring,
similar to pipedash's secret management.
"""

import keyring
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class KeyringManager:
    """
    Manages secure storage of API tokens using system keyring.
    
    Uses platform-specific keyring:
    - macOS: Keychain
    - Linux: Secret Service (libsecret)
    - Windows: Credential Manager
    """
    
    SERVICE_NAME = "flowforge"
    
    @classmethod
    def set_token(cls, provider_name: str, token: str) -> bool:
        """
        Store a token securely in keyring.
        
        Args:
            provider_name: Name of the provider (e.g., 'github', 'gitlab')
            token: API token to store
            
        Returns:
            bool: True if successful
        """
        try:
            key = f"{provider_name}_token"
            keyring.set_password(cls.SERVICE_NAME, key, token)
            logger.info(f"Token stored for provider: {provider_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to store token for {provider_name}: {e}")
            return False
    
    @classmethod
    def get_token(cls, provider_name: str) -> Optional[str]:
        """
        Retrieve a token from keyring.
        
        Args:
            provider_name: Name of the provider
            
        Returns:
            Token string or None if not found
        """
        try:
            key = f"{provider_name}_token"
            token = keyring.get_password(cls.SERVICE_NAME, key)
            return token
        except Exception as e:
            logger.error(f"Failed to retrieve token for {provider_name}: {e}")
            return None
    
    @classmethod
    def delete_token(cls, provider_name: str) -> bool:
        """
        Delete a token from keyring.
        
        Args:
            provider_name: Name of the provider
            
        Returns:
            bool: True if successful
        """
        try:
            key = f"{provider_name}_token"
            keyring.delete_password(cls.SERVICE_NAME, key)
            logger.info(f"Token deleted for provider: {provider_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete token for {provider_name}: {e}")
            return False
    
    @classmethod
    def has_token(cls, provider_name: str) -> bool:
        """
        Check if a token exists in keyring.
        
        Args:
            provider_name: Name of the provider
            
        Returns:
            bool: True if token exists
        """
        token = cls.get_token(provider_name)
        return token is not None
    
    @classmethod
    def set_provider_config(cls, provider_name: str, config_key: str, value: str) -> bool:
        """
        Store provider configuration value securely.
        
        Args:
            provider_name: Name of the provider
            config_key: Configuration key
            value: Configuration value
            
        Returns:
            bool: True if successful
        """
        try:
            key = f"{provider_name}_{config_key}"
            keyring.set_password(cls.SERVICE_NAME, key, value)
            return True
        except Exception as e:
            logger.error(f"Failed to store config for {provider_name}.{config_key}: {e}")
            return False
    
    @classmethod
    def get_provider_config(cls, provider_name: str, config_key: str) -> Optional[str]:
        """
        Retrieve provider configuration value.
        
        Args:
            provider_name: Name of the provider
            config_key: Configuration key
            
        Returns:
            Configuration value or None
        """
        try:
            key = f"{provider_name}_{config_key}"
            value = keyring.get_password(cls.SERVICE_NAME, key)
            return value
        except Exception as e:
            logger.error(f"Failed to retrieve config for {provider_name}.{config_key}: {e}")
            return None


"""
Custom exceptions for FlowForge.

Provides specific exception types for different error scenarios.
"""


class FlowForgeError(Exception):
    """Base exception for FlowForge errors."""
    pass


class ProviderError(FlowForgeError):
    """Exception raised for provider-related errors."""
    
    def __init__(self, message: str, provider_name: str = None):
        super().__init__(message)
        self.provider_name = provider_name


class ValidationError(FlowForgeError):
    """Exception raised for validation errors."""
    pass


class AuthenticationError(FlowForgeError):
    """Exception raised for authentication errors."""
    pass


class ConfigurationError(FlowForgeError):
    """Exception raised for configuration errors."""
    pass


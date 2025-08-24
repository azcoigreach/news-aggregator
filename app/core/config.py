"""
Configuration management for the News Aggregator application.

IMPORTANT: Configuration Architecture
=====================================

This application uses a two-tier configuration system:

1. BOOTSTRAP CONFIGURATION (this file):
   - Only contains minimal settings required to start the application
   - Database connection, Redis connection, basic server settings
   - Should be deployment-specific, not user-specific
   - Configured via bootstrap.conf file or environment variables

2. API-DRIVEN CONFIGURATION:
   - All user-configurable settings (API keys, crawling preferences, etc.)
   - Stored in database and managed through REST API endpoints
   - Can be changed at runtime without restart
   - Provides web UI for configuration management

DEVELOPMENT PRINCIPLE: 
- Backend should have MINIMAL configuration needed to bootstrap
- Everything else should be configurable through the API/UI
- No .env files for user settings
"""
from typing import Optional, Any
from .bootstrap_config import bootstrap_settings


def get_config_service():
    """Lazy import to avoid circular dependencies."""
    from ..services.configuration_service import config_service
    return config_service


def get_api_configuration(key: str, category: str = None, default: Any = None) -> Any:
    """
    Get configuration from API-driven configuration service.
    
    Args:
        key: Configuration key
        category: Optional category filter  
        default: Default value if not found
        
    Returns:
        Configuration value from database or default
    """
    try:
        config_service = get_config_service()
        return config_service.get_configuration(key, category, default)
    except ImportError:
        # During startup, service may not be available yet
        return default


def set_api_configuration(
    key: str, 
    value: Any, 
    category: str,
    description: str = None,
    changed_by: str = "api"
) -> bool:
    """
    Set configuration value through API-driven configuration service.
    
    Args:
        key: Configuration key
        value: Configuration value
        category: Configuration category
        description: Optional description
        changed_by: Who made the change
        
    Returns:
        True if successful
    """
    try:
        config_service = get_config_service()
        return config_service.set_configuration(
            key=key,
            value=value, 
            category=category,
            description=description,
            changed_by=changed_by
        )
    except ImportError:
        # During startup, service may not be available yet
        return False


class ApplicationSettings:
    """
    Application settings that combine bootstrap and API-driven configuration.
    
    This class provides a unified interface to access both bootstrap settings
    (required to start the app) and API-driven settings (user-configurable).
    """
    
    def __init__(self):
        self.bootstrap = bootstrap_settings
    
    # Bootstrap settings (passthrough)
    @property
    def app_name(self) -> str:
        return self.bootstrap.app_name
    
    @property 
    def version(self) -> str:
        return self.bootstrap.version
        
    @property
    def host(self) -> str:
        return self.bootstrap.host
        
    @property
    def port(self) -> int:
        return self.bootstrap.port
        
    @property
    def debug(self) -> bool:
        return self.bootstrap.debug
        
    @property
    def log_level(self) -> str:
        return self.bootstrap.log_level
        
    @property
    def secret_key(self) -> str:
        # Try to get from API config first, fallback to bootstrap
        api_secret = get_api_configuration("secret_key", "security")
        return api_secret if api_secret else self.bootstrap.secret_key
    
    @property
    def database(self):
        return self.bootstrap.database
        
    @property
    def redis(self):
        return self.bootstrap.redis
        
    @property
    def celery(self):
        return self.bootstrap.celery
    
    # API-driven settings
    @property
    def openai_api_key(self) -> Optional[str]:
        return get_api_configuration("openai_api_key", "ai_models", "")
    
    @property
    def openai_model(self) -> str:
        return get_api_configuration("openai_model", "ai_models", "gpt-4")
    
    @property
    def claude_api_key(self) -> Optional[str]:
        return get_api_configuration("claude_api_key", "ai_models", "")
    
    @property
    def claude_model(self) -> str:
        return get_api_configuration("claude_model", "ai_models", "claude-3-sonnet-20240229")
    
    @property
    def crawler_user_agent(self) -> str:
        return get_api_configuration("crawler_user_agent", "crawler", "NewsAggregator/1.0")
    
    @property
    def crawler_delay(self) -> float:
        return get_api_configuration("crawler_delay", "crawler", 1.0)
    
    @property
    def max_concurrent_requests(self) -> int:
        return get_api_configuration("max_concurrent_requests", "crawler", 16)
    
    @property
    def fact_check_confidence_threshold(self) -> float:
        return get_api_configuration("fact_check_confidence_threshold", "fact_checker", 0.8)
    
    @property
    def max_verification_attempts(self) -> int:
        return get_api_configuration("max_verification_attempts", "fact_checker", 3)
    
    def initialize_defaults(self):
        """Initialize default API-driven configurations."""
        try:
            config_service = get_config_service()
            config_service.initialize_default_configurations()
        except ImportError:
            # During startup, service may not be available yet
            pass


# Global settings instance
settings = ApplicationSettings()

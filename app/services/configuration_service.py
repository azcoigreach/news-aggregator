"""
API-driven configuration service for News Aggregator.

This service manages all user-configurable settings through the database and API.
Settings are stored in the Configuration model and can be updated at runtime.
"""
from typing import Dict, Any, Optional, List, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_
import json
from datetime import datetime

from ..models.configuration import Configuration
from ..core.database import get_db_context


class ConfigurationService:
    """Service for managing API-driven configuration."""
    
    def __init__(self):
        self._cache = {}
        self._cache_timestamp = None
        self._cache_ttl = 300  # 5 minutes cache TTL
    
    def get_configuration(self, key: str, category: str = None, default: Any = None) -> Any:
        """
        Get a configuration value by key.
        
        Args:
            key: Configuration key
            category: Optional category filter
            default: Default value if not found
            
        Returns:
            Configuration value or default
        """
        with get_db_context() as db:
            query = db.query(Configuration).filter(
                and_(
                    Configuration.key == key,
                    Configuration.is_active == True
                )
            )
            
            if category:
                query = query.filter(Configuration.category == category)
            
            config = query.first()
            
            if config:
                return config.value
            
            return default
    
    def set_configuration(
        self, 
        key: str, 
        value: Any, 
        category: str,
        description: str = None,
        value_type: str = "auto",
        changed_by: str = "api"
    ) -> bool:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
            category: Configuration category
            description: Optional description
            value_type: Value type (auto-detected if not specified)
            changed_by: Who made the change
            
        Returns:
            True if successful
        """
        if value_type == "auto":
            value_type = self._detect_value_type(value)
        
        with get_db_context() as db:
            # Check if configuration exists
            existing = db.query(Configuration).filter(
                Configuration.key == key
            ).first()
            
            if existing:
                # Update existing configuration
                existing.previous_value = existing.value
                existing.value = value
                existing.value_type = value_type
                existing.changed_by = changed_by
                existing.change_reason = f"Updated via API by {changed_by}"
                existing.updated_at = datetime.utcnow()
            else:
                # Create new configuration
                config = Configuration(
                    key=key,
                    category=category,
                    description=description or f"Configuration for {key}",
                    value=value,
                    value_type=value_type,
                    changed_by=changed_by,
                    change_reason=f"Created via API by {changed_by}"
                )
                db.add(config)
            
            db.commit()
            self._clear_cache()
            return True
    
    def get_category_configurations(self, category: str) -> Dict[str, Any]:
        """
        Get all configurations for a category.
        
        Args:
            category: Configuration category
            
        Returns:
            Dictionary of key-value pairs
        """
        with get_db_context() as db:
            configs = db.query(Configuration).filter(
                and_(
                    Configuration.category == category,
                    Configuration.is_active == True
                )
            ).all()
            
            return {config.key: config.value for config in configs}
    
    def get_all_categories(self) -> List[str]:
        """Get list of all configuration categories."""
        with get_db_context() as db:
            categories = db.query(Configuration.category).distinct().all()
            return [cat[0] for cat in categories]
    
    def delete_configuration(self, key: str) -> bool:
        """
        Delete a configuration (mark as inactive).
        
        Args:
            key: Configuration key
            
        Returns:
            True if successful
        """
        with get_db_context() as db:
            config = db.query(Configuration).filter(
                Configuration.key == key
            ).first()
            
            if config:
                config.is_active = False
                db.commit()
                self._clear_cache()
                return True
            
            return False
    
    def initialize_default_configurations(self):
        """Initialize default configurations on first startup."""
        defaults = [
            # AI Model Configurations
            {
                "key": "openai_api_key",
                "category": "ai_models",
                "value": "",
                "description": "OpenAI API key for fact checking",
                "value_type": "string",
                "is_sensitive": True
            },
            {
                "key": "openai_model",
                "category": "ai_models", 
                "value": "gpt-4",
                "description": "OpenAI model to use",
                "value_type": "string"
            },
            {
                "key": "claude_api_key",
                "category": "ai_models",
                "value": "",
                "description": "Claude API key for fact checking",
                "value_type": "string",
                "is_sensitive": True
            },
            {
                "key": "claude_model",
                "category": "ai_models",
                "value": "claude-3-sonnet-20240229",
                "description": "Claude model to use",
                "value_type": "string"
            },
            
            # Crawler Configurations
            {
                "key": "crawler_user_agent",
                "category": "crawler",
                "value": "NewsAggregator/1.0",
                "description": "User agent for web crawling",
                "value_type": "string"
            },
            {
                "key": "crawler_delay",
                "category": "crawler",
                "value": 1.0,
                "description": "Delay between requests in seconds",
                "value_type": "float"
            },
            {
                "key": "max_concurrent_requests",
                "category": "crawler",
                "value": 16,
                "description": "Maximum concurrent crawling requests",
                "value_type": "integer"
            },
            
            # Fact Checker Configurations
            {
                "key": "fact_check_confidence_threshold",
                "category": "fact_checker",
                "value": 0.8,
                "description": "Minimum confidence threshold for fact checking",
                "value_type": "float"
            },
            {
                "key": "max_verification_attempts",
                "category": "fact_checker",
                "value": 3,
                "description": "Maximum verification attempts per article",
                "value_type": "integer"
            },
            
            # System Configurations
            {
                "key": "system_initialized",
                "category": "system",
                "value": True,
                "description": "Whether system has been initialized",
                "value_type": "boolean"
            }
        ]
        
        for default_config in defaults:
            existing = self.get_configuration(default_config["key"], default_config["category"])
            if existing is None:
                self.set_configuration(
                    key=default_config["key"],
                    value=default_config["value"],
                    category=default_config["category"],
                    description=default_config["description"],
                    value_type=default_config["value_type"],
                    changed_by="system_init"
                )
    
    def _detect_value_type(self, value: Any) -> str:
        """Auto-detect value type."""
        if isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, (list, dict)):
            return "json"
        else:
            return "string"
    
    def _clear_cache(self):
        """Clear configuration cache."""
        self._cache = {}
        self._cache_timestamp = None


# Global configuration service instance
config_service = ConfigurationService()
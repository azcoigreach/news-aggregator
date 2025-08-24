"""
Bootstrap configuration for News Aggregator.

This module contains ONLY the minimal configuration required to start the application.
All user-configurable settings should be managed through the API.

Bootstrap Configuration Principles:
1. Only include settings required to connect to database and start services
2. No API keys, user preferences, or business logic configuration
3. Settings should be deployment-specific, not user-specific
4. Values should have sensible defaults for development
"""
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseBootstrapSettings(BaseSettings):
    """Minimal database configuration required to start the application."""
    url: str = Field(
        default="postgresql://postgres:password@localhost:5432/news_aggregator",
        description="Database connection URL - deployment specific"
    )
    echo: bool = Field(
        default=False,
        description="Enable SQL query logging for debugging"
    )
    pool_size: int = Field(
        default=10,
        description="Database connection pool size"
    )
    max_overflow: int = Field(
        default=20,
        description="Maximum database connection overflow"
    )
    
    model_config = {"env_prefix": "DATABASE_"}


class RedisBootstrapSettings(BaseSettings):
    """Minimal Redis configuration required for task queue."""
    url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL for task queue"
    )
    
    model_config = {"env_prefix": "REDIS_"}


class CeleryBootstrapSettings(BaseSettings):
    """Minimal Celery configuration required for background tasks."""
    broker_url: str = Field(
        default="redis://localhost:6379/0",
        description="Celery broker URL"
    )
    result_backend: str = Field(
        default="redis://localhost:6379/0",
        description="Celery result backend URL"
    )
    
    model_config = {"env_prefix": "CELERY_"}


class ApplicationBootstrapSettings(BaseSettings):
    """Bootstrap application settings - minimal configuration to start the app."""
    
    # Application identity
    app_name: str = Field(
        default="News Aggregator",
        description="Application name"
    )
    version: str = Field(
        default="0.1.0",
        description="Application version"
    )
    
    # Server configuration
    host: str = Field(
        default="0.0.0.0",
        description="Host to bind the server to"
    )
    port: int = Field(
        default=8000,
        description="Port to bind the server to"
    )
    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )
    
    # Security - minimal for bootstrap
    secret_key: str = Field(
        default="bootstrap-secret-key-replace-via-api",
        description="Secret key for JWT tokens - should be changed via API"
    )
    
    # Logging
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    
    # Service connections
    database: DatabaseBootstrapSettings = Field(
        default_factory=DatabaseBootstrapSettings,
        description="Database connection settings"
    )
    redis: RedisBootstrapSettings = Field(
        default_factory=RedisBootstrapSettings,
        description="Redis connection settings"
    )
    celery: CeleryBootstrapSettings = Field(
        default_factory=CeleryBootstrapSettings,
        description="Celery task queue settings"
    )
    
    model_config = {
        "env_file": "bootstrap.conf",  # Use .conf file instead of .env
        "env_file_encoding": "utf-8",
        "case_sensitive": False
    }


# Global bootstrap settings instance
bootstrap_settings = ApplicationBootstrapSettings()
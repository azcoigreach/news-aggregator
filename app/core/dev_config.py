"""
Development configuration for the News Aggregator application.
This file contains settings that are specific to development environments.
"""
from .config import settings


class DevelopmentSettings:
    """Development-specific settings."""
    
    # Override production settings for development
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    
    # Development database (SQLite for easier local development)
    DATABASE_URL = "sqlite:///./dev_news_aggregator.db"
    
    # Development Redis (local instance)
    REDIS_URL = "redis://localhost:6379/0"
    
    # Development Celery
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
    
    # Development AI settings (use test keys or local models)
    OPENAI_API_KEY = None  # Set in environment or via API
    CLAUDE_API_KEY = None  # Set in environment or via API
    
    # Development MCP settings
    MCP_ENABLED = True
    MCP_SERVERS = ["localhost:3000"]  # Local MCP server
    
    # Development crawler settings
    CRAWLER_REQUEST_DELAY = 0.1  # Faster for development
    CRAWLER_MAX_CONCURRENT_REQUESTS = 4  # Lower for development
    
    # Development fact checker settings
    FACT_CHECKER_CONFIDENCE_THRESHOLD = 0.7  # Lower for development
    FACT_CHECKER_MAX_VERIFICATION_ATTEMPTS = 2  # Lower for development


# Development settings instance
dev_settings = DevelopmentSettings()

"""
Configuration management for the News Aggregator application.
"""
from typing import List, Optional
from pydantic import BaseSettings, Field, validator
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    url: str = Field(default="postgresql://postgres:password@localhost:5432/news_aggregator")
    echo: bool = Field(default=False)
    pool_size: int = Field(default=10)
    max_overflow: int = Field(default=20)
    
    class Config:
        env_prefix = "DATABASE_"


class RedisSettings(BaseSettings):
    """Redis configuration settings."""
    url: str = Field(default="redis://localhost:6379/0")
    host: str = Field(default="localhost")
    port: int = Field(default=6379)
    db: int = Field(default=0)
    password: Optional[str] = Field(default=None)
    
    class Config:
        env_prefix = "REDIS_"


class CelerySettings(BaseSettings):
    """Celery configuration settings."""
    broker_url: str = Field(default="redis://localhost:6379/0")
    result_backend: str = Field(default="redis://localhost:6379/0")
    task_serializer: str = Field(default="json")
    result_serializer: str = Field(default="json")
    accept_content: List[str] = Field(default=["json"])
    timezone: str = Field(default="UTC")
    enable_utc: bool = Field(default=True)
    
    class Config:
        env_prefix = "CELERY_"


class OpenAISettings(BaseSettings):
    """OpenAI API configuration settings."""
    api_key: Optional[str] = Field(default=None)
    model: str = Field(default="gpt-4")
    max_tokens: int = Field(default=2000)
    temperature: float = Field(default=0.1)
    
    class Config:
        env_prefix = "OPENAI_"


class ClaudeSettings(BaseSettings):
    """Claude API configuration settings."""
    api_key: Optional[str] = Field(default=None)
    model: str = Field(default="claude-3-sonnet-20240229")
    max_tokens: int = Field(default=2000)
    temperature: float = Field(default=0.1)
    
    class Config:
        env_prefix = "CLAUDE_"


class MCPSettings(BaseSettings):
    """MCP configuration settings."""
    enabled: bool = Field(default=True)
    servers: List[str] = Field(default=[])
    timeout: int = Field(default=30)
    
    class Config:
        env_prefix = "MCP_"


class CrawlerSettings(BaseSettings):
    """Web crawler configuration settings."""
    user_agent: str = Field(default="NewsAggregator/1.0")
    request_delay: float = Field(default=1.0)
    max_concurrent_requests: int = Field(default=16)
    download_timeout: int = Field(default=30)
    retry_times: int = Field(default=3)
    
    class Config:
        env_prefix = "CRAWLER_"


class FactCheckerSettings(BaseSettings):
    """Fact checker configuration settings."""
    confidence_threshold: float = Field(default=0.8)
    max_verification_attempts: int = Field(default=3)
    cross_reference_sources: int = Field(default=5)
    enable_llm_validation: bool = Field(default=True)
    
    class Config:
        env_prefix = "FACT_CHECKER_"


class AppSettings(BaseSettings):
    """Main application configuration settings."""
    # Application
    app_name: str = Field(default="News Aggregator")
    version: str = Field(default="0.1.0")
    debug: bool = Field(default=False)
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    
    # Security
    secret_key: str = Field(default="your-secret-key-change-in-production")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    
    # Logging
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="json")
    
    # Database
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    
    # Redis
    redis: RedisSettings = Field(default_factory=RedisSettings)
    
    # Celery
    celery: CelerySettings = Field(default_factory=CelerySettings)
    
    # AI Models
    openai: OpenAISettings = Field(default_factory=OpenAISettings)
    claude: ClaudeSettings = Field(default_factory=ClaudeSettings)
    
    # MCP
    mcp: MCPSettings = Field(default_factory=MCPSettings)
    
    # Crawler
    crawler: CrawlerSettings = Field(default_factory=CrawlerSettings)
    
    # Fact Checker
    fact_checker: FactCheckerSettings = Field(default_factory=FactCheckerSettings)
    
    @validator("secret_key")
    def validate_secret_key(cls, v):
        if v == "your-secret-key-change-in-production":
            import secrets
            return secrets.token_urlsafe(32)
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = AppSettings()

"""
Source model for managing news sources.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class Source(Base):
    """Source model for news outlets and feeds."""
    
    __tablename__ = "sources"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic source information
    name = Column(String(255), nullable=False, unique=True, index=True)
    url = Column(String(1000), nullable=False, unique=True, index=True)
    rss_url = Column(String(1000), nullable=True)
    description = Column(Text, nullable=True)
    
    # Source configuration
    source_type = Column(String(50), nullable=False, default="website")  # website, rss, api
    active = Column(Boolean, default=True, nullable=False)
    priority = Column(Integer, default=1, nullable=False)  # 1-10 priority scale
    
    # Crawling configuration
    crawl_frequency = Column(Integer, default=300, nullable=False)  # seconds
    max_articles_per_crawl = Column(Integer, default=50, nullable=False)
    respect_robots_txt = Column(Boolean, default=True, nullable=False)
    crawl_delay = Column(Float, default=1.0, nullable=False)  # seconds
    
    # Quality metrics
    reliability_score = Column(Float, nullable=True)  # 0.0 to 1.0
    success_rate = Column(Float, nullable=True)       # 0.0 to 1.0
    average_response_time = Column(Float, nullable=True)  # milliseconds
    
    # Access configuration
    requires_auth = Column(Boolean, default=False, nullable=False)
    api_key = Column(String(500), nullable=True)
    user_agent = Column(String(255), nullable=True)
    headers = Column(JSON, nullable=True)  # Additional headers
    
    # Processing configuration
    content_selectors = Column(JSON, nullable=True)  # CSS selectors for content extraction
    title_selector = Column(String(255), nullable=True)
    author_selector = Column(String(255), nullable=True)
    date_selector = Column(String(255), nullable=True)
    
    # Status tracking
    last_crawled_at = Column(DateTime(timezone=True), nullable=True)
    last_success_at = Column(DateTime(timezone=True), nullable=True)
    last_error_at = Column(DateTime(timezone=True), nullable=True)
    last_error_message = Column(Text, nullable=True)
    consecutive_errors = Column(Integer, default=0, nullable=False)
    
    # Statistics
    total_articles_crawled = Column(Integer, default=0, nullable=False)
    articles_crawled_today = Column(Integer, default=0, nullable=False)
    
    # Metadata
    language = Column(String(10), default="en", nullable=False)
    country = Column(String(2), nullable=True)  # ISO country code
    category = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Source(id={self.id}, name='{self.name}', url='{self.url}', active={self.active})>"
    
    def to_dict(self):
        """Convert source to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "rss_url": self.rss_url,
            "description": self.description,
            "source_type": self.source_type,
            "active": self.active,
            "priority": self.priority,
            "crawl_frequency": self.crawl_frequency,
            "max_articles_per_crawl": self.max_articles_per_crawl,
            "respect_robots_txt": self.respect_robots_txt,
            "crawl_delay": self.crawl_delay,
            "reliability_score": self.reliability_score,
            "success_rate": self.success_rate,
            "average_response_time": self.average_response_time,
            "requires_auth": self.requires_auth,
            "language": self.language,
            "country": self.country,
            "category": self.category,
            "last_crawled_at": self.last_crawled_at.isoformat() if self.last_crawled_at else None,
            "last_success_at": self.last_success_at.isoformat() if self.last_success_at else None,
            "last_error_at": self.last_error_at.isoformat() if self.last_error_at else None,
            "last_error_message": self.last_error_message,
            "consecutive_errors": self.consecutive_errors,
            "total_articles_crawled": self.total_articles_crawled,
            "articles_crawled_today": self.articles_crawled_today,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
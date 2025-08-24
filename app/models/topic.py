"""
Topic model for managing news topics and keywords.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class Topic(Base):
    """Topic model for news aggregation."""
    
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    keywords = Column(JSON, nullable=False, default=list)  # List of keywords
    sources = Column(JSON, nullable=False, default=list)   # List of source URLs
    active = Column(Boolean, default=True, nullable=False)
    priority = Column(Integer, default=1, nullable=False)  # 1-10 priority scale
    
    # Crawling configuration
    crawl_frequency = Column(Integer, default=300, nullable=False)  # seconds
    max_articles_per_crawl = Column(Integer, default=100, nullable=False)
    
    # AI processing configuration
    enable_fact_checking = Column(Boolean, default=True, nullable=False)
    enable_summarization = Column(Boolean, default=True, nullable=False)
    enable_correlation = Column(Boolean, default=True, nullable=False)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_crawled_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    articles = relationship("Article", back_populates="topic")
    
    def __repr__(self):
        return f"<Topic(id={self.id}, name='{self.name}', active={self.active})>"
    
    def to_dict(self):
        """Convert topic to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "keywords": self.keywords,
            "sources": self.sources,
            "active": self.active,
            "priority": self.priority,
            "crawl_frequency": self.crawl_frequency,
            "max_articles_per_crawl": self.max_articles_per_crawl,
            "enable_fact_checking": self.enable_fact_checking,
            "enable_summarization": self.enable_summarization,
            "enable_correlation": self.enable_correlation,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_crawled_at": self.last_crawled_at.isoformat() if self.last_crawled_at else None,
        }

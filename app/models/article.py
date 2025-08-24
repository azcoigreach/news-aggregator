"""
Article model for storing news articles and their metadata.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class Article(Base):
    """Article model for news content."""
    
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic article information
    title = Column(String(500), nullable=False, index=True)
    content = Column(Text, nullable=False)
    url = Column(String(1000), nullable=False, unique=True, index=True)
    source_url = Column(String(1000), nullable=False, index=True)
    author = Column(String(255), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    
    # Content processing
    summary = Column(Text, nullable=True)
    keywords_extracted = Column(JSON, nullable=True)  # List of extracted keywords
    sentiment_score = Column(Float, nullable=True)    # -1.0 to 1.0
    
    # Processing status
    is_processed = Column(Boolean, default=False, nullable=False)
    is_fact_checked = Column(Boolean, default=False, nullable=False)
    is_summarized = Column(Boolean, default=False, nullable=False)
    is_correlated = Column(Boolean, default=False, nullable=False)
    
    # Quality metrics
    readability_score = Column(Float, nullable=True)
    credibility_score = Column(Float, nullable=True)
    
    # Metadata
    language = Column(String(10), default="en", nullable=False)
    word_count = Column(Integer, nullable=True)
    reading_time = Column(Integer, nullable=True)  # minutes
    
    # Relationships
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    topic = relationship("Topic", back_populates="articles")
    
    fact_checks = relationship("FactCheck", back_populates="article")
    summaries = relationship("Summary", back_populates="article")
    correlations = relationship("Correlation", back_populates="article", foreign_keys="[Correlation.article_id]")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    crawled_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title[:50]}...', source='{self.source_url}')>"
    
    def to_dict(self):
        """Convert article to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "url": self.url,
            "source_url": self.source_url,
            "author": self.author,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "summary": self.summary,
            "keywords_extracted": self.keywords_extracted,
            "sentiment_score": self.sentiment_score,
            "is_processed": self.is_processed,
            "is_fact_checked": self.is_fact_checked,
            "is_summarized": self.is_summarized,
            "is_correlated": self.is_correlated,
            "readability_score": self.readability_score,
            "credibility_score": self.credibility_score,
            "language": self.language,
            "word_count": self.word_count,
            "reading_time": self.reading_time,
            "topic_id": self.topic_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "crawled_at": self.crawled_at.isoformat() if self.crawled_at else None,
        }

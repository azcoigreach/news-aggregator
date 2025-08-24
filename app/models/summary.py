"""
Summary model for storing article summaries.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class Summary(Base):
    """Summary model for article summaries."""
    
    __tablename__ = "summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    article = relationship("Article", back_populates="summaries")
    
    # Summary content
    summary_type = Column(String(50), nullable=False, default="standard")  # standard, brief, detailed, bullet_points
    summary_text = Column(Text, nullable=False)
    key_points = Column(JSON, nullable=True)  # List of key points
    
    # Summary metadata
    word_count = Column(Integer, nullable=True)
    sentence_count = Column(Integer, nullable=True)
    compression_ratio = Column(Float, nullable=True)  # original_length / summary_length
    reading_time = Column(Integer, nullable=True)  # minutes
    
    # AI model information
    model_used = Column(String(100), nullable=True)  # AI model used for generation
    model_version = Column(String(50), nullable=True)
    generation_parameters = Column(JSON, nullable=True)  # Parameters used for generation
    
    # Quality metrics
    quality_score = Column(Float, nullable=True)  # 0.0 to 1.0
    coherence_score = Column(Float, nullable=True)  # How coherent is the summary
    coverage_score = Column(Float, nullable=True)   # How well does it cover the original
    factual_accuracy = Column(Float, nullable=True)  # Factual accuracy compared to original
    
    # Processing information
    processing_time = Column(Float, nullable=True)  # Processing time in seconds
    retry_count = Column(Integer, default=0, nullable=False)
    error_messages = Column(JSON, nullable=True)  # Any errors encountered
    
    # Additional features
    entities_mentioned = Column(JSON, nullable=True)  # Named entities in summary
    topics_covered = Column(JSON, nullable=True)      # Topics covered in summary
    sentiment_score = Column(Float, nullable=True)    # Sentiment of the summary
    
    # Status and validation
    is_validated = Column(Boolean, default=False, nullable=False)
    validation_score = Column(Float, nullable=True)
    human_reviewed = Column(Boolean, default=False, nullable=False)
    approved = Column(Boolean, default=True, nullable=False)
    
    # Language and localization
    language = Column(String(10), default="en", nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    validated_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Summary(id={self.id}, article_id={self.article_id}, type='{self.summary_type}', words={self.word_count})>"
    
    def to_dict(self):
        """Convert summary to dictionary."""
        return {
            "id": self.id,
            "article_id": self.article_id,
            "summary_type": self.summary_type,
            "summary_text": self.summary_text,
            "key_points": self.key_points,
            "word_count": self.word_count,
            "sentence_count": self.sentence_count,
            "compression_ratio": self.compression_ratio,
            "reading_time": self.reading_time,
            "model_used": self.model_used,
            "model_version": self.model_version,
            "generation_parameters": self.generation_parameters,
            "quality_score": self.quality_score,
            "coherence_score": self.coherence_score,
            "coverage_score": self.coverage_score,
            "factual_accuracy": self.factual_accuracy,
            "processing_time": self.processing_time,
            "retry_count": self.retry_count,
            "error_messages": self.error_messages,
            "entities_mentioned": self.entities_mentioned,
            "topics_covered": self.topics_covered,
            "sentiment_score": self.sentiment_score,
            "is_validated": self.is_validated,
            "validation_score": self.validation_score,
            "human_reviewed": self.human_reviewed,
            "approved": self.approved,
            "language": self.language,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "validated_at": self.validated_at.isoformat() if self.validated_at else None,
        }
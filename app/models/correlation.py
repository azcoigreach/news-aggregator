"""
Correlation model for storing article relationships and clustering.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class Correlation(Base):
    """Correlation model for article relationships."""
    
    __tablename__ = "correlations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Primary article relationship
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    article = relationship("Article", back_populates="correlations", foreign_keys=[article_id])
    
    # Related article information
    related_article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    
    # Correlation metrics
    correlation_type = Column(String(50), nullable=False)  # semantic, topical, temporal, source
    similarity_score = Column(Float, nullable=False)  # 0.0 to 1.0
    confidence_level = Column(Float, nullable=False)  # 0.0 to 1.0
    
    # Similarity details
    semantic_similarity = Column(Float, nullable=True)    # Semantic content similarity
    topical_similarity = Column(Float, nullable=True)     # Topic/category similarity
    temporal_proximity = Column(Float, nullable=True)     # Time-based proximity
    source_similarity = Column(Float, nullable=True)      # Source-based similarity
    
    # Common elements
    shared_keywords = Column(JSON, nullable=True)         # Common keywords
    shared_entities = Column(JSON, nullable=True)         # Common named entities
    shared_topics = Column(JSON, nullable=True)           # Common topics
    shared_sources = Column(JSON, nullable=True)          # Common source references
    
    # Cluster information
    cluster_id = Column(String(100), nullable=True)       # Cluster identifier
    cluster_size = Column(Integer, nullable=True)         # Size of the cluster
    cluster_centroid = Column(Boolean, default=False, nullable=False)  # Is this the cluster center
    
    # Temporal analysis
    time_difference = Column(Float, nullable=True)        # Time difference in hours
    trend_direction = Column(String(20), nullable=True)   # rising, stable, declining
    viral_potential = Column(Float, nullable=True)        # Potential for viral spread
    
    # Analysis metadata
    analysis_method = Column(String(100), nullable=True)  # Method used for correlation
    algorithm_version = Column(String(50), nullable=True)
    processing_time = Column(Float, nullable=True)        # Processing time in seconds
    
    # Quality and validation
    manual_validation = Column(Boolean, default=False, nullable=False)
    validation_score = Column(Float, nullable=True)       # Human validation score
    false_positive_flag = Column(Boolean, default=False, nullable=False)
    
    # Status tracking
    is_active = Column(Boolean, default=True, nullable=False)
    needs_review = Column(Boolean, default=False, nullable=False)
    review_reason = Column(String(255), nullable=True)
    
    # Additional insights
    narrative_connection = Column(Text, nullable=True)    # Textual description of connection
    implications = Column(JSON, nullable=True)           # Potential implications
    recommended_actions = Column(JSON, nullable=True)    # Recommended follow-up actions
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    validated_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Correlation(id={self.id}, article_id={self.article_id}, related_id={self.related_article_id}, type='{self.correlation_type}', score={self.similarity_score})>"
    
    def to_dict(self):
        """Convert correlation to dictionary."""
        return {
            "id": self.id,
            "article_id": self.article_id,
            "related_article_id": self.related_article_id,
            "correlation_type": self.correlation_type,
            "similarity_score": self.similarity_score,
            "confidence_level": self.confidence_level,
            "semantic_similarity": self.semantic_similarity,
            "topical_similarity": self.topical_similarity,
            "temporal_proximity": self.temporal_proximity,
            "source_similarity": self.source_similarity,
            "shared_keywords": self.shared_keywords,
            "shared_entities": self.shared_entities,
            "shared_topics": self.shared_topics,
            "shared_sources": self.shared_sources,
            "cluster_id": self.cluster_id,
            "cluster_size": self.cluster_size,
            "cluster_centroid": self.cluster_centroid,
            "time_difference": self.time_difference,
            "trend_direction": self.trend_direction,
            "viral_potential": self.viral_potential,
            "analysis_method": self.analysis_method,
            "algorithm_version": self.algorithm_version,
            "processing_time": self.processing_time,
            "manual_validation": self.manual_validation,
            "validation_score": self.validation_score,
            "false_positive_flag": self.false_positive_flag,
            "is_active": self.is_active,
            "needs_review": self.needs_review,
            "review_reason": self.review_reason,
            "narrative_connection": self.narrative_connection,
            "implications": self.implications,
            "recommended_actions": self.recommended_actions,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "validated_at": self.validated_at.isoformat() if self.validated_at else None,
        }
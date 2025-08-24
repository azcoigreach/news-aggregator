"""
Fact check model for storing fact verification results.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class FactCheck(Base):
    """Fact check model for article verification results."""
    
    __tablename__ = "fact_checks"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    article = relationship("Article", back_populates="fact_checks")
    
    # Fact check results
    verification_status = Column(String(50), nullable=False, default="pending")  # pending, verified, disputed, false, unknown
    confidence_score = Column(Float, nullable=True)  # 0.0 to 1.0
    overall_rating = Column(String(50), nullable=True)  # true, mostly_true, mixed, mostly_false, false
    
    # AI model results
    openai_result = Column(JSON, nullable=True)
    claude_result = Column(JSON, nullable=True)
    mcp_results = Column(JSON, nullable=True)  # Results from MCP servers
    
    # Verification details
    fact_claims = Column(JSON, nullable=True)  # List of extracted fact claims
    verified_claims = Column(JSON, nullable=True)  # Claims that were verified
    disputed_claims = Column(JSON, nullable=True)  # Claims that were disputed
    unverified_claims = Column(JSON, nullable=True)  # Claims that couldn't be verified
    
    # Sources and references
    sources_checked = Column(JSON, nullable=True)  # List of sources consulted
    cross_references = Column(JSON, nullable=True)  # Cross-reference results
    external_fact_checks = Column(JSON, nullable=True)  # External fact-check sources
    
    # Processing information
    processing_time = Column(Float, nullable=True)  # Processing time in seconds
    models_used = Column(JSON, nullable=True)  # List of AI models used
    error_messages = Column(JSON, nullable=True)  # Any errors encountered
    
    # Quality metrics
    source_credibility = Column(Float, nullable=True)  # Average credibility of sources
    claim_complexity = Column(Float, nullable=True)    # Complexity of claims being checked
    verification_depth = Column(Integer, nullable=True)  # Number of verification steps
    
    # Flags and warnings
    flags = Column(JSON, nullable=True)  # List of flags raised during fact-checking
    warnings = Column(JSON, nullable=True)  # Warnings about verification quality
    needs_human_review = Column(Boolean, default=False, nullable=False)
    
    # Status tracking
    is_completed = Column(Boolean, default=False, nullable=False)
    retry_count = Column(Integer, default=0, nullable=False)
    last_retry_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<FactCheck(id={self.id}, article_id={self.article_id}, status='{self.verification_status}', confidence={self.confidence_score})>"
    
    def to_dict(self):
        """Convert fact check to dictionary."""
        return {
            "id": self.id,
            "article_id": self.article_id,
            "verification_status": self.verification_status,
            "confidence_score": self.confidence_score,
            "overall_rating": self.overall_rating,
            "openai_result": self.openai_result,
            "claude_result": self.claude_result,
            "mcp_results": self.mcp_results,
            "fact_claims": self.fact_claims,
            "verified_claims": self.verified_claims,
            "disputed_claims": self.disputed_claims,
            "unverified_claims": self.unverified_claims,
            "sources_checked": self.sources_checked,
            "cross_references": self.cross_references,
            "external_fact_checks": self.external_fact_checks,
            "processing_time": self.processing_time,
            "models_used": self.models_used,
            "error_messages": self.error_messages,
            "source_credibility": self.source_credibility,
            "claim_complexity": self.claim_complexity,
            "verification_depth": self.verification_depth,
            "flags": self.flags,
            "warnings": self.warnings,
            "needs_human_review": self.needs_human_review,
            "is_completed": self.is_completed,
            "retry_count": self.retry_count,
            "last_retry_at": self.last_retry_at.isoformat() if self.last_retry_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
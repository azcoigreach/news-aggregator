"""
Configuration model for storing application settings.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Float
from sqlalchemy.sql import func

from ..core.database import Base


class Configuration(Base):
    """Configuration model for application settings."""
    
    __tablename__ = "configurations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Configuration identification
    key = Column(String(255), nullable=False, unique=True, index=True)
    category = Column(String(100), nullable=False, index=True)  # crawler, ai, fact_checker, etc.
    description = Column(Text, nullable=True)
    
    # Configuration values
    value = Column(JSON, nullable=False)  # The actual configuration value
    default_value = Column(JSON, nullable=True)  # Default value for reference
    value_type = Column(String(50), nullable=False)  # string, integer, float, boolean, json, list
    
    # Validation and constraints
    min_value = Column(Float, nullable=True)      # For numeric values
    max_value = Column(Float, nullable=True)      # For numeric values
    allowed_values = Column(JSON, nullable=True)  # List of allowed values
    validation_regex = Column(String(500), nullable=True)  # Regex for string validation
    
    # Configuration metadata
    is_sensitive = Column(Boolean, default=False, nullable=False)  # Contains sensitive data
    requires_restart = Column(Boolean, default=False, nullable=False)  # Requires app restart
    is_readonly = Column(Boolean, default=False, nullable=False)   # Cannot be modified
    is_system = Column(Boolean, default=False, nullable=False)     # System configuration
    
    # Environment and scope
    environment = Column(String(50), default="all", nullable=False)  # dev, prod, test, all
    scope = Column(String(50), default="global", nullable=False)     # global, user, session
    
    # Change tracking
    previous_value = Column(JSON, nullable=True)  # Previous value for rollback
    changed_by = Column(String(255), nullable=True)  # User who made the change
    change_reason = Column(Text, nullable=True)   # Reason for the change
    
    # Status and lifecycle
    is_active = Column(Boolean, default=True, nullable=False)
    is_deprecated = Column(Boolean, default=False, nullable=False)
    deprecation_message = Column(Text, nullable=True)
    removal_date = Column(DateTime(timezone=True), nullable=True)
    
    # Grouping and organization
    group_name = Column(String(100), nullable=True)  # Logical grouping
    display_order = Column(Integer, default=0, nullable=False)  # Display order in UI
    display_name = Column(String(255), nullable=True)  # Human-readable name
    
    # Documentation
    help_text = Column(Text, nullable=True)       # Help text for users
    example_value = Column(JSON, nullable=True)   # Example value
    related_configs = Column(JSON, nullable=True) # Related configuration keys
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_accessed_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Configuration(id={self.id}, key='{self.key}', category='{self.category}', value={self.value})>"
    
    def to_dict(self, include_sensitive=False):
        """Convert configuration to dictionary."""
        result = {
            "id": self.id,
            "key": self.key,
            "category": self.category,
            "description": self.description,
            "default_value": self.default_value,
            "value_type": self.value_type,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "allowed_values": self.allowed_values,
            "validation_regex": self.validation_regex,
            "is_sensitive": self.is_sensitive,
            "requires_restart": self.requires_restart,
            "is_readonly": self.is_readonly,
            "is_system": self.is_system,
            "environment": self.environment,
            "scope": self.scope,
            "changed_by": self.changed_by,
            "change_reason": self.change_reason,
            "is_active": self.is_active,
            "is_deprecated": self.is_deprecated,
            "deprecation_message": self.deprecation_message,
            "removal_date": self.removal_date.isoformat() if self.removal_date else None,
            "group_name": self.group_name,
            "display_order": self.display_order,
            "display_name": self.display_name,
            "help_text": self.help_text,
            "example_value": self.example_value,
            "related_configs": self.related_configs,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_accessed_at": self.last_accessed_at.isoformat() if self.last_accessed_at else None,
        }
        
        # Include sensitive values only if explicitly requested
        if include_sensitive or not self.is_sensitive:
            result["value"] = self.value
            result["previous_value"] = self.previous_value
        else:
            result["value"] = "***HIDDEN***"
            result["previous_value"] = "***HIDDEN***"
            
        return result
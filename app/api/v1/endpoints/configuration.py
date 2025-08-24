"""
Configuration endpoint for managing application settings through API.

IMPORTANT: This endpoint manages USER-CONFIGURABLE settings only.
Bootstrap settings (database, Redis connections) are not exposed here.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.services.configuration_service import config_service

router = APIRouter()


class ConfigurationRequest(BaseModel):
    """Request model for configuration updates."""
    key: str = Field(..., description="Configuration key")
    value: Any = Field(..., description="Configuration value")
    category: str = Field(..., description="Configuration category")
    description: Optional[str] = Field(None, description="Configuration description")


class ConfigurationResponse(BaseModel):
    """Response model for configuration data."""
    key: str
    value: Any
    category: str
    description: Optional[str]
    value_type: str
    is_sensitive: bool
    updated_at: Optional[str]


@router.get("/", response_model=Dict[str, Any])
async def get_all_configurations(
    include_sensitive: bool = False,
    db: Session = Depends(get_db)
):
    """
    Get all user-configurable settings organized by category.
    
    Args:
        include_sensitive: Whether to include sensitive values (API keys, etc.)
        
    Returns:
        Dict containing all configurations organized by category
    """
    try:
        categories = config_service.get_all_categories()
        result = {}
        
        for category in categories:
            # Skip system categories that shouldn't be exposed
            if category in ["system", "bootstrap"]:
                continue
                
            category_configs = config_service.get_category_configurations(category)
            result[category] = category_configs
            
        return {
            "status": "success",
            "configurations": result,
            "message": "Configurations retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve configurations: {str(e)}"
        )


@router.get("/categories", response_model=List[str])
async def get_configuration_categories(db: Session = Depends(get_db)):
    """
    Get list of all configuration categories.
    
    Returns:
        List of category names
    """
    try:
        categories = config_service.get_all_categories()
        # Filter out system categories
        user_categories = [cat for cat in categories if cat not in ["system", "bootstrap"]]
        return user_categories
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve categories: {str(e)}"
        )


@router.get("/category/{category}", response_model=Dict[str, Any])
async def get_category_configurations(
    category: str,
    db: Session = Depends(get_db)
):
    """
    Get all configurations for a specific category.
    
    Args:
        category: Configuration category
        
    Returns:
        Dict containing all configurations in the category
    """
    if category in ["system", "bootstrap"]:
        raise HTTPException(
            status_code=403,
            detail="Access to system configurations is forbidden"
        )
    
    try:
        configurations = config_service.get_category_configurations(category)
        return {
            "category": category,
            "configurations": configurations,
            "count": len(configurations)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve category configurations: {str(e)}"
        )


@router.get("/{key}", response_model=Dict[str, Any])
async def get_configuration(
    key: str,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get a specific configuration value.
    
    Args:
        key: Configuration key
        category: Optional category filter
        
    Returns:
        Configuration value and metadata
    """
    try:
        value = config_service.get_configuration(key, category)
        if value is None:
            raise HTTPException(
                status_code=404,
                detail=f"Configuration '{key}' not found"
            )
        
        return {
            "key": key,
            "value": value,
            "category": category,
            "message": "Configuration retrieved successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve configuration: {str(e)}"
        )


@router.post("/", response_model=Dict[str, Any])
async def set_configuration(
    config_request: ConfigurationRequest,
    db: Session = Depends(get_db)
):
    """
    Set a configuration value.
    
    Args:
        config_request: Configuration data
        
    Returns:
        Success message
    """
    if config_request.category in ["system", "bootstrap"]:
        raise HTTPException(
            status_code=403,
            detail="Cannot modify system or bootstrap configurations via API"
        )
    
    try:
        success = config_service.set_configuration(
            key=config_request.key,
            value=config_request.value,
            category=config_request.category,
            description=config_request.description,
            changed_by="api_user"
        )
        
        if success:
            return {
                "status": "success",
                "message": f"Configuration '{config_request.key}' updated successfully"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to update configuration"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to set configuration: {str(e)}"
        )


@router.put("/{key}", response_model=Dict[str, Any])
async def update_configuration(
    key: str,
    config_request: ConfigurationRequest,
    db: Session = Depends(get_db)
):
    """
    Update an existing configuration value.
    
    Args:
        key: Configuration key to update
        config_request: New configuration data
        
    Returns:
        Success message
    """
    if config_request.category in ["system", "bootstrap"]:
        raise HTTPException(
            status_code=403,
            detail="Cannot modify system or bootstrap configurations via API"
        )
    
    # Ensure the key matches
    if key != config_request.key:
        raise HTTPException(
            status_code=400,
            detail="Key in URL must match key in request body"
        )
    
    try:
        # Check if configuration exists
        existing = config_service.get_configuration(key, config_request.category)
        if existing is None:
            raise HTTPException(
                status_code=404,
                detail=f"Configuration '{key}' not found"
            )
        
        success = config_service.set_configuration(
            key=config_request.key,
            value=config_request.value,
            category=config_request.category,
            description=config_request.description,
            changed_by="api_user"
        )
        
        if success:
            return {
                "status": "success",
                "message": f"Configuration '{key}' updated successfully"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to update configuration"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update configuration: {str(e)}"
        )


@router.delete("/{key}", response_model=Dict[str, Any])
async def delete_configuration(
    key: str,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Delete a configuration (mark as inactive).
    
    Args:
        key: Configuration key to delete
        category: Optional category for validation
        
    Returns:
        Success message
    """
    try:
        # Check if configuration exists and validate category
        existing = config_service.get_configuration(key, category)
        if existing is None:
            raise HTTPException(
                status_code=404,
                detail=f"Configuration '{key}' not found"
            )
        
        success = config_service.delete_configuration(key)
        
        if success:
            return {
                "status": "success",
                "message": f"Configuration '{key}' deleted successfully"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to delete configuration"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete configuration: {str(e)}"
        )


@router.post("/initialize", response_model=Dict[str, Any])
async def initialize_default_configurations(db: Session = Depends(get_db)):
    """
    Initialize default configurations.
    
    This endpoint sets up all default user-configurable settings.
    Should typically be called once after application setup.
    
    Returns:
        Success message
    """
    try:
        config_service.initialize_default_configurations()
        return {
            "status": "success",
            "message": "Default configurations initialized successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize configurations: {str(e)}"
        )


@router.get("/ai-models/status", response_model=Dict[str, Any])
async def get_ai_models_status(db: Session = Depends(get_db)):
    """
    Get status of AI model configurations.
    
    Returns:
        Status of all configured AI models
    """
    try:
        openai_key = config_service.get_configuration("openai_api_key", "ai_models", "")
        claude_key = config_service.get_configuration("claude_api_key", "ai_models", "")
        
        return {
            "openai": {
                "configured": bool(openai_key),
                "model": config_service.get_configuration("openai_model", "ai_models", "gpt-4")
            },
            "claude": {
                "configured": bool(claude_key),
                "model": config_service.get_configuration("claude_model", "ai_models", "claude-3-sonnet-20240229")
            },
            "status": "ready" if (openai_key or claude_key) else "needs_configuration"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get AI models status: {str(e)}"
        )
# Configuration Architecture

## Overview

The News Aggregator uses a **two-tier configuration system** that cleanly separates infrastructure configuration from user-configurable settings.

## Configuration Principles

### 🎯 **Core Principle**
- **Backend should have MINIMAL configuration** needed to bootstrap
- **Everything else should be configurable through the API/UI**
- **No .env files for user settings**

### 🏗️ **Two-Tier Architecture**

#### 1. Bootstrap Configuration
**Purpose**: Contains only the minimal settings required to start the application
**Location**: `bootstrap.conf` file or environment variables
**Scope**: Deployment-specific, infrastructure settings
**Managed by**: System administrators, deployment tools

**Contents**:
- Database connection URL
- Redis connection URL
- Server host/port
- Basic security settings
- Logging configuration

**Example**:
```bash
# Essential service connections only
DATABASE_URL=postgresql://postgres:password@postgres:5432/news_aggregator
REDIS_URL=redis://redis:6379/0
HOST=0.0.0.0
PORT=8000
```

#### 2. API-Driven Configuration
**Purpose**: All user-configurable application settings
**Location**: Database (Configuration model)
**Scope**: User preferences, business logic settings
**Managed by**: Users through REST API endpoints

**Contents**:
- AI model API keys and preferences
- Crawling settings and schedules
- Fact-checking parameters
- Source configurations
- Processing rules

## Implementation

### Bootstrap Configuration (`app/core/bootstrap_config.py`)

```python
class ApplicationBootstrapSettings(BaseSettings):
    """Bootstrap settings - minimal configuration to start the app."""
    
    # Only essential infrastructure settings
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    database: DatabaseBootstrapSettings = Field(default_factory=DatabaseBootstrapSettings)
    redis: RedisBootstrapSettings = Field(default_factory=RedisBootstrapSettings)
    
    model_config = {"env_file": "bootstrap.conf"}
```

### API Configuration Service (`app/services/configuration_service.py`)

```python
class ConfigurationService:
    """Service for managing API-driven configuration."""
    
    def get_configuration(self, key: str, category: str = None, default: Any = None):
        """Get configuration from database."""
        
    def set_configuration(self, key: str, value: Any, category: str):
        """Set configuration in database."""
```

### Unified Settings (`app/core/config.py`)

```python
class ApplicationSettings:
    """Unified interface combining bootstrap and API-driven config."""
    
    def __init__(self):
        self.bootstrap = bootstrap_settings
    
    # Bootstrap settings (passthrough)
    @property
    def host(self) -> str:
        return self.bootstrap.host
    
    # API-driven settings (from database)
    @property
    def openai_api_key(self) -> str:
        return get_api_configuration("openai_api_key", "ai_models", "")
```

## API Endpoints

### Configuration Management
- `GET /api/v1/configuration/` - Get all user configurations
- `POST /api/v1/configuration/` - Set configuration value
- `PUT /api/v1/configuration/{key}` - Update configuration
- `DELETE /api/v1/configuration/{key}` - Delete configuration
- `GET /api/v1/configuration/categories` - List configuration categories

### Category-Specific Endpoints
- `GET /api/v1/configuration/category/{category}` - Get category configurations
- `GET /api/v1/configuration/ai-models/status` - AI model configuration status
- `POST /api/v1/configuration/initialize` - Initialize default configurations

## Usage Examples

### Setting API Keys
```bash
# Set OpenAI API key
curl -X POST "http://localhost:8000/api/v1/configuration/" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "openai_api_key",
    "value": "sk-your-api-key-here",
    "category": "ai_models",
    "description": "OpenAI API key for fact checking"
  }'
```

### Configuring Crawling Settings
```bash
# Set crawler delay
curl -X POST "http://localhost:8000/api/v1/configuration/" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "crawler_delay",
    "value": 2.0,
    "category": "crawler",
    "description": "Delay between requests in seconds"
  }'
```

### Getting Configuration Status
```bash
# Get all AI model configurations
curl "http://localhost:8000/api/v1/configuration/category/ai_models"

# Get AI models status
curl "http://localhost:8000/api/v1/configuration/ai-models/status"
```

## Configuration Categories

### AI Models (`ai_models`)
- `openai_api_key` - OpenAI API key
- `openai_model` - OpenAI model name (default: gpt-4)
- `claude_api_key` - Claude API key
- `claude_model` - Claude model name

### Crawler (`crawler`)
- `crawler_user_agent` - User agent string
- `crawler_delay` - Delay between requests
- `max_concurrent_requests` - Maximum concurrent requests

### Fact Checker (`fact_checker`)
- `fact_check_confidence_threshold` - Minimum confidence threshold
- `max_verification_attempts` - Maximum verification attempts

### System (`system`)
- Internal system configurations (not user-editable)

## Development Guidelines

### ✅ **DO**
- Add new user settings to API-driven configuration
- Use the ConfigurationService for runtime settings
- Document configuration changes in this file
- Initialize sensible defaults in `initialize_default_configurations()`

### ❌ **DON'T**
- Add user settings to bootstrap configuration
- Use environment variables for user preferences
- Hardcode configuration values in application code
- Expose system/bootstrap configurations through API

### Adding New Configuration

1. **Define the setting in ConfigurationService defaults**:
```python
{
    "key": "new_setting",
    "category": "appropriate_category",
    "value": "default_value",
    "description": "What this setting controls",
    "value_type": "string"
}
```

2. **Add property to ApplicationSettings**:
```python
@property
def new_setting(self) -> str:
    return get_api_configuration("new_setting", "appropriate_category", "default_value")
```

3. **Update documentation** in this file

## Security Considerations

### Sensitive Values
- API keys and secrets are marked as `is_sensitive=True`
- Sensitive values are hidden in API responses unless explicitly requested
- Use proper authentication for configuration endpoints (TODO)

### Access Control
- System and bootstrap configurations are not exposed through API
- Consider implementing role-based access for configuration management

## Bootstrap File Format

The `bootstrap.conf` file uses simple key=value format:

```bash
# Comments are supported
APP_NAME=News Aggregator
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://host:port/db

# No user settings should be added here!
```

## Migration from Environment Variables

If migrating from `.env` approach:

1. **Keep infrastructure settings** in `bootstrap.conf`
2. **Move user settings** to API configuration:
   ```bash
   # Initialize defaults
   curl -X POST "http://localhost:8000/api/v1/configuration/initialize"
   
   # Set specific values
   curl -X POST "http://localhost:8000/api/v1/configuration/" -d '{"key":"setting","value":"value","category":"category"}'
   ```

## Benefits

### 🎯 **Clean Separation**
- Infrastructure vs. user configuration clearly separated
- Deployment settings isolated from business logic

### 🔄 **Runtime Updates**
- Configuration changes without application restart
- Dynamic reconfiguration through API

### 🛡️ **Security**
- Sensitive values properly managed
- API-based access control possible

### 📊 **Auditability**
- All configuration changes tracked in database
- Change history and rollback capability

### 🎛️ **User Experience**
- Web UI for configuration management
- Validation and help text for settings
- Organized by functional categories

## Future Enhancements

- Web UI for configuration management
- Role-based access control
- Configuration validation and constraints
- Import/export of configuration sets
- Configuration templates for different deployment types
# News Aggregator

A Python-based autonomous news aggregation and fact-checking application that crawls the internet for news on user-selected topics, verifies information using AI models, and provides summarized, fact-checked content.

## 🚀 Features

- **Intelligent News Crawling**: Automated discovery of news articles from multiple sources
- **AI-Powered Fact Checking**: Multi-model verification using OpenAI GPT-4 and Claude
- **Content Correlation**: Find related stories and fact patterns across sources
- **Smart Summarization**: AI-generated summaries with fact-check results
- **MCP Integration**: Model Context Protocol for external AI model interactions
- **RESTful API**: Comprehensive FastAPI with Swagger documentation
- **Autonomous Operation**: Background processing with task queues
- **Configuration Management**: API-driven configuration system

## 🏗️ Architecture

### Core Components

1. **News Crawler Service**
   - Web scraping and RSS feed monitoring
   - Configurable source management
   - Content extraction and cleaning

2. **Content Processor**
   - Article parsing and metadata extraction
   - Content normalization and storage
   - Duplicate detection

3. **Fact Checker Engine**
   - AI-powered verification using multiple models
   - Confidence scoring and validation
   - Cross-reference checking

4. **Correlation Engine**
   - Related story discovery
   - Fact pattern recognition
   - Timeline analysis

5. **API Layer**
   - FastAPI with comprehensive Swagger docs
   - RESTful endpoints for all operations
   - Real-time status monitoring

6. **MCP Integration**
   - External AI model connections
   - Model switching and fallback
   - Performance monitoring

## 🛠️ Technology Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy
- **Database**: PostgreSQL
- **Task Queue**: Redis + Celery
- **AI Models**: OpenAI GPT-4, Claude, local models via MCP
- **Web Scraping**: Scrapy, BeautifulSoup, Newspaper3k
- **Testing**: pytest, pytest-asyncio, pytest-cov
- **Containerization**: Docker + Docker Compose
- **Monitoring**: Prometheus + Grafana

## 📦 Installation

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- OpenAI API key (for fact checking)
- Claude API key (optional)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd news-aggregator
   ```

2. **Start the application**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Manual Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up database**
   ```bash
   # PostgreSQL setup commands
   ```

3. **Configure API keys**
   ```bash
   # Set via API endpoints
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

## 🔧 Configuration

### API Configuration

The application uses an API-driven configuration system. All user settings are managed through REST endpoints:

- **Topics**: Define news topics to monitor
- **Sources**: Configure news sources and crawling parameters
- **AI Models**: Set API keys and model preferences
- **Processing Rules**: Configure fact-checking and summarization parameters

### Backend Configuration

Core functionality settings are maintained in configuration files:

- Database connections
- Task queue settings
- Default crawling parameters
- System limits and timeouts

## 📚 API Documentation

### Core Endpoints

- `GET /topics` - List configured topics
- `POST /topics` - Create new topic
- `GET /articles` - Retrieve articles
- `GET /articles/{id}` - Get specific article with fact-check results
- `POST /crawl` - Trigger manual crawling
- `GET /status` - System status and health

### Swagger Documentation

Comprehensive API documentation is available at `/docs` when the application is running.

## 🧪 Testing

### Test Strategy

- **Unit Tests**: Individual component testing
- **Integration Tests**: Service interaction testing
- **API Tests**: Endpoint functionality testing
- **End-to-End Tests**: Complete workflow testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/api/
```

## 🐳 Docker

### Services

- **app**: Main FastAPI application
- **postgres**: PostgreSQL database
- **redis**: Redis for task queue
- **celery**: Background task worker
- **nginx**: Reverse proxy (optional)

### Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔍 Usage Examples

### 1. Setting Up a Topic

```bash
curl -X POST "http://localhost:8000/topics" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Technology",
    "keywords": ["artificial intelligence", "machine learning", "AI"],
    "sources": ["techcrunch.com", "wired.com"],
    "active": true
  }'
```

### 2. Retrieving Articles

```bash
curl "http://localhost:8000/articles?topic=AI%20Technology&limit=10"
```

### 3. Manual Crawling

```bash
curl -X POST "http://localhost:8000/crawl" \
  -H "Content-Type: application/json" \
  -d '{"topic_id": "123", "force": true}'
```

## 📊 Monitoring

### Health Checks

- Application health: `/health`
- Database connectivity: `/health/db`
- Task queue status: `/health/queue`

### Metrics

- Crawling performance
- Fact-checking accuracy
- API response times
- System resource usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Implement the feature
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

[License information]

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation
- Review the test suite for usage examples

## 🔮 Roadmap

- [ ] Enhanced fact-checking algorithms
- [ ] Multi-language support
- [ ] Advanced correlation analysis
- [ ] Real-time news alerts
- [ ] User authentication and personalization
- [ ] Mobile application
- [ ] Advanced analytics dashboard

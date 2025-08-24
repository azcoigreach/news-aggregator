#!/bin/bash

# Development setup script for News Aggregator
# This script sets up the development environment

set -e

echo "🚀 Setting up News Aggregator development environment..."

# Check if Python 3.11+ is installed
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.11+ is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Install development dependencies
echo "🔧 Installing development dependencies..."
pip install pytest pytest-asyncio pytest-cov black isort flake8 mypy

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p data
mkdir -p docker/postgres
mkdir -p docker/nginx
mkdir -p docker/prometheus
mkdir -p docker/grafana

# Check if Docker is installed
if command -v docker &> /dev/null; then
    echo "✅ Docker is installed"
    
    # Check if Docker Compose is installed
    if command -v docker-compose &> /dev/null; then
        echo "✅ Docker Compose is installed"
        
        # Build Docker images
        echo "🐳 Building Docker images..."
        docker-compose build
        
        echo "🐳 Starting services..."
        docker-compose up -d postgres redis
        
        # Wait for services to be ready
        echo "⏳ Waiting for services to be ready..."
        sleep 10
        
        # Check service health
        echo "🔍 Checking service health..."
        if docker-compose ps | grep -q "Up"; then
            echo "✅ Services are running"
        else
            echo "❌ Services failed to start"
            docker-compose logs
            exit 1
        fi
        
    else
        echo "⚠️ Docker Compose not found. Please install it to use Docker services."
    fi
else
    echo "⚠️ Docker not found. Please install Docker to use containerized services."
fi

# Initialize database
echo "🗄️ Initializing database..."
python -c "
from app.core.database import init_db
init_db()
print('Database initialized successfully')
"

# Run tests to verify setup
echo "🧪 Running tests to verify setup..."
pytest tests/test_health.py -v

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Start the application: python -m app.main"
echo "3. Access API documentation: http://localhost:8000/docs"
echo "4. Run tests: pytest"
echo "5. Start Docker services: docker-compose up -d"
echo ""
echo "Happy coding! 🚀"

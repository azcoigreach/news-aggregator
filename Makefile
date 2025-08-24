# Makefile for News Aggregator development

.PHONY: help setup test run clean docker-up docker-down docker-logs lint format

# Default target
help:
	@echo "News Aggregator Development Commands:"
	@echo ""
	@echo "Setup:"
	@echo "  setup          - Set up development environment"
	@echo "  install        - Install Python dependencies"
	@echo ""
	@echo "Development:"
	@echo "  run            - Run the application locally"
	@echo "  test           - Run all tests"
	@echo "  test-unit      - Run unit tests only"
	@echo "  test-api       - Run API tests only"
	@echo "  test-cov       - Run tests with coverage report"
	@echo ""
	@echo "Docker:"
	@echo "  docker-up      - Start all Docker services"
	@echo "  docker-down    - Stop all Docker services"
	@echo "  docker-logs    - View Docker service logs"
	@echo "  docker-build   - Build Docker images"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint           - Run linting checks"
	@echo "  format         - Format code with black and isort"
	@echo "  type-check     - Run type checking with mypy"
	@echo ""
	@echo "Database:"
	@echo "  db-init        - Initialize database"
	@echo "  db-migrate     - Run database migrations"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean          - Clean up generated files"
	@echo "  clean-docker   - Clean up Docker containers and volumes"

# Setup
setup:
	@echo "Setting up development environment..."
	@./scripts/setup_dev.sh

install:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Development
run:
	@echo "Starting News Aggregator application..."
	python -m app.main

# Testing
test:
	@echo "Running all tests..."
	pytest

test-unit:
	@echo "Running unit tests..."
	pytest tests/unit/ -v

test-api:
	@echo "Running API tests..."
	pytest tests/api/ -v

test-cov:
	@echo "Running tests with coverage..."
	pytest --cov=app --cov-report=html --cov-report=term-missing

# Docker
docker-up:
	@echo "Starting Docker services..."
	docker-compose up -d

docker-down:
	@echo "Stopping Docker services..."
	docker-compose down

docker-logs:
	@echo "Viewing Docker service logs..."
	docker-compose logs -f

docker-build:
	@echo "Building Docker images..."
	docker-compose build

# Code Quality
lint:
	@echo "Running linting checks..."
	flake8 app/ tests/
	pylint app/ tests/

format:
	@echo "Formatting code..."
	black app/ tests/
	isort app/ tests/

type-check:
	@echo "Running type checks..."
	mypy app/

# Database
db-init:
	@echo "Initializing database..."
	python -c "from app.core.database import init_db; init_db()"

db-migrate:
	@echo "Running database migrations..."
	alembic upgrade head

# Cleanup
clean:
	@echo "Cleaning up generated files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf dist/
	rm -rf build/

clean-docker:
	@echo "Cleaning up Docker containers and volumes..."
	docker-compose down -v
	docker system prune -f
	docker volume prune -f

# Development workflow
dev: format lint test
	@echo "Development checks completed successfully!"

# Quick start for new developers
quickstart: setup docker-up db-init
	@echo "Quick start completed! Run 'make run' to start the application."

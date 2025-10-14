.PHONY: help install dev test lint format clean docker-build docker-up docker-down \
        test-cov test-unit test-integration check security update-deps

help:
	@echo "Available commands:"
	@echo "  make install          - Install dependencies"
	@echo "  make dev              - Run development server"
	@echo "  make test             - Run all tests"
	@echo "  make test-cov         - Run tests with coverage report"
	@echo "  make test-unit        - Run unit tests only"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make lint             - Run linting (flake8 + mypy)"
	@echo "  make format           - Format code with black"
	@echo "  make check            - Run all checks (format + lint + test)"
	@echo "  make security         - Run security checks"
	@echo "  make clean            - Clean cache files"
	@echo "  make docker-build     - Build Docker image"
	@echo "  make docker-up        - Start Docker containers"
	@echo "  make docker-down      - Stop Docker containers"
	@echo "  make update-deps      - Update dependencies"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	TESTING=true pytest

test-cov:
	TESTING=true pytest --cov=app --cov-report=html --cov-report=term

test-unit:
	TESTING=true pytest tests/unit/ -v

test-integration:
	TESTING=true pytest tests/integration/ -v

lint:
	@echo "Running flake8..."
	flake8 app tests --max-line-length=100 --exclude=__pycache__
	@echo "Running mypy..."
	mypy app --ignore-missing-imports

format:
	black app tests --line-length=100

check: format lint test
	@echo "✅ All checks passed!"

security:
	@echo "Checking for security vulnerabilities..."
	pip install safety bandit
	safety check
	bandit -r app

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf .mypy_cache
	@echo "✅ Cleaned cache files"

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d
	@echo "✅ Services started"
	@echo "API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-restart:
	docker-compose restart

update-deps:
	pip install --upgrade pip
	pip list --outdated
	@echo "To update all packages: pip install -U -r requirements.txt"

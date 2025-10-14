# 🔧 Troubleshooting Guide

This guide helps you resolve common issues when working with the Quantitative Trading Engine.

## Table of Contents
- [Installation Issues](#installation-issues)
- [Database Issues](#database-issues)
- [API Issues](#api-issues)
- [Testing Issues](#testing-issues)
- [Docker Issues](#docker-issues)
- [Performance Issues](#performance-issues)

## Installation Issues

### Issue: `pip install` fails with dependency conflicts

**Solution:**
```bash
# Create a fresh virtual environment
python -m venv venv_new
source venv_new/bin/activate  # On Windows: venv_new\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Issue: Import errors when running examples

**Error:** `ModuleNotFoundError: No module named 'app'`

**Solution:**
```bash
# Make sure you're in the project root directory
cd quantitative-trading-engine

# Run examples from the root directory
python examples/simple_backtest.py

# Or add the project to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## Database Issues

### Issue: Database connection failed

**Error:** `sqlalchemy.exc.OperationalError: could not connect to server`

**Solution:**

1. **Check if PostgreSQL is running:**
```bash
# On Linux/Mac
sudo systemctl status postgresql

# Or use Docker
docker-compose ps
```

2. **Verify database credentials in `.env`:**
```bash
# Check your .env file
cat .env | grep DATABASE_URL

# Default should be:
DATABASE_URL=postgresql://trading:trading123@localhost:5432/trading_db
```

3. **Create database if it doesn't exist:**
```bash
# Using psql
psql -U postgres -c "CREATE DATABASE trading_db;"

# Or use Docker
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE trading_db;"
```

### Issue: Database migrations not working

**Solution:**
```bash
# Drop and recreate all tables (WARNING: This deletes all data!)
python -c "from app.core.database import engine, Base; Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine)"

# Or restart Docker containers
docker-compose down -v
docker-compose up -d
```

## API Issues

### Issue: API returns 500 Internal Server Error

**Solution:**

1. **Check the logs:**
```bash
# If running with uvicorn
# Check terminal output for error messages

# If running with Docker
docker-compose logs -f api
```

2. **Verify all dependencies are installed:**
```bash
pip install -r requirements.txt
```

3. **Check database connection:**
```bash
# Test database connectivity
python -c "from app.core.database import engine; print(engine.connect())"
```

### Issue: CORS errors in browser

**Error:** `Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy`

**Solution:**

Edit `app/core/config.py` and update CORS origins:
```python
BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]
```

### Issue: API endpoint not found (404)

**Common mistakes:**
- Missing `/api/v1` prefix
- Incorrect HTTP method (GET vs POST)
- Typo in endpoint name

**Solution:**
```bash
# Check available endpoints at:
http://localhost:8000/docs

# Correct endpoint format:
POST http://localhost:8000/api/v1/strategies/
GET  http://localhost:8000/api/v1/strategies/{id}
```

## Testing Issues

### Issue: Tests fail with database errors

**Error:** `TESTING environment variable not set`

**Solution:**
```bash
# Run tests with TESTING flag
TESTING=true pytest

# Or add to pytest.ini
[pytest]
env = 
    TESTING=true
```

### Issue: Import errors in tests

**Solution:**
```bash
# Make sure pytest is installed
pip install pytest pytest-cov pytest-asyncio

# Run from project root
cd /path/to/quantitative-trading-engine
pytest
```

### Issue: Tests pass locally but fail in CI

**Solution:**
- Ensure all test dependencies are in `requirements.txt`
- Check Python version compatibility
- Verify environment variables are set in CI configuration

## Docker Issues

### Issue: Docker containers won't start

**Solution:**

1. **Check Docker daemon:**
```bash
docker info
```

2. **Check for port conflicts:**
```bash
# Check if ports are already in use
lsof -i :8000  # API port
lsof -i :5432  # PostgreSQL port
lsof -i :6379  # Redis port
```

3. **Rebuild containers:**
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Issue: Database data persists after docker-compose down

**Solution:**
```bash
# Remove volumes to delete all data
docker-compose down -v

# Or remove specific volumes
docker volume ls
docker volume rm quantitative-trading-engine_postgres_data
```

### Issue: Permission denied errors in Docker

**Solution:**
```bash
# On Linux, add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Or run with sudo
sudo docker-compose up -d
```

## Performance Issues

### Issue: Backtest takes too long

**Solutions:**

1. **Reduce data size:**
```python
# Use smaller date ranges
start_date = datetime.now() - timedelta(days=30)  # Instead of 365
```

2. **Optimize strategy parameters:**
```python
# Use shorter moving average periods
parameters = {
    'fast_period': 5,   # Instead of 50
    'slow_period': 15   # Instead of 200
}
```

3. **Use sampling:**
```python
# Sample data for faster testing
data_sampled = data.iloc[::5]  # Every 5th row
```

### Issue: High memory usage

**Solution:**

1. **Process data in chunks:**
```python
# For large datasets
chunk_size = 1000
for chunk in pd.read_csv('data.csv', chunksize=chunk_size):
    process(chunk)
```

2. **Use data types efficiently:**
```python
# Convert to appropriate dtypes
df['volume'] = df['volume'].astype('int32')
df['price'] = df['price'].astype('float32')
```

## Market Data Issues

### Issue: Yahoo Finance API returns empty data

**Possible causes:**
- Invalid ticker symbol
- No data for the date range
- API rate limiting

**Solution:**
```python
# Verify ticker symbol
import yfinance as yf
ticker = yf.Ticker("AAPL")
print(ticker.info)

# Use broader date range
start_date = datetime.now() - timedelta(days=365)

# Add error handling
try:
    data = yf.download("AAPL", start=start_date, end=datetime.now())
    if data.empty:
        print("No data returned for this symbol/date range")
except Exception as e:
    print(f"Error fetching data: {e}")
```

### Issue: Rate limiting from data provider

**Solution:**
```python
# Add delays between requests
import time

for symbol in symbols:
    data = fetch_data(symbol)
    time.sleep(1)  # Wait 1 second between requests
```

## Common Error Messages

### `RuntimeError: Event loop is closed`

**Solution:**
```python
# Use pytest-asyncio for async tests
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

### `DeprecationWarning: declarative_base() is deprecated`

**Solution:**
Already fixed in the codebase. Update to the latest version:
```bash
git pull origin main
pip install -r requirements.txt
```

### `AttributeError: 'NoneType' object has no attribute`

**Common in strategy backtests when data is insufficient**

**Solution:**
```python
# Ensure enough data for indicators
min_periods = max(fast_period, slow_period) + 10
if len(data) < min_periods:
    raise ValueError(f"Need at least {min_periods} data points")
```

## Getting Help

If you're still experiencing issues:

1. **Check existing issues:** [GitHub Issues](https://github.com/galafis/quantitative-trading-engine/issues)
2. **Search discussions:** Look for similar problems in discussions
3. **Create a new issue:** Provide:
   - Error message (full stack trace)
   - Steps to reproduce
   - Environment details (OS, Python version)
   - Configuration files (without sensitive data)

## Debugging Tips

### Enable Debug Logging

```python
# Add to your code
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Inspect Variables

```python
# Use pdb for debugging
import pdb; pdb.set_trace()

# Or use print debugging
print(f"Data shape: {data.shape}")
print(f"Strategy params: {strategy.parameters}")
```

### Check Data Quality

```python
# Verify data before backtesting
print(data.info())
print(data.describe())
print(data.isnull().sum())

# Check for duplicates
print(data.duplicated().sum())
```

---

**Need more help?** Open an issue on [GitHub](https://github.com/galafis/quantitative-trading-engine/issues) with details about your problem.

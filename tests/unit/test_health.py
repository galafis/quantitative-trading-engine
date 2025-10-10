import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "timestamp" in response.json()
    assert response.json()["service"] == "Quantitative Trading Engine"

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Quantitative Trading Engine API"
    assert response.json()["version"] == "1.0.0"
    assert response.json()["docs"] == "/docs"


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "timestamp" in response.json()
    assert response.json()["service"] == "Quantitative Trading Engine"


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Quantitative Trading Engine API"
    assert response.json()["version"] == "1.0.0"
    assert response.json()["docs"] == "/docs"

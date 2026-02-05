# tests/test_api.py
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test du endpoint /health"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "rag-it-assistant"
    }

def test_query_endpoint_without_auth():
    """Test que /query nécessite l'authentification"""
    response = client.post("/query", json={"question": "Test"})
    assert response.status_code == 401  # Unauthorized
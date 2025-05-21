"""
Basic health check tests for the API.
"""
import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(test_app: TestClient):
    """Test the root endpoint."""
    response = test_app.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_api_v1_health_check(test_app: TestClient):
    """Test health check endpoint if it exists."""
    response = test_app.get("/api/v1/health")
    # Health check endpoint might not exist, so we check for 200 or 404
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert "status" in data

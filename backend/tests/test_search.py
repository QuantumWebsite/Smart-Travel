"""
Tests for search endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from tests.utils import create_random_user, get_auth_headers, create_search_data


def test_create_search(test_app: TestClient, test_db: Session):
    """Test creating a new search."""
    # Create a user
    user = create_random_user(test_db)
    
    # Get authentication headers
    headers = get_auth_headers(user.id)
    
    # Create search data
    search_data = create_search_data(user.id)
    
    # Make the request
    response = test_app.post("/api/v1/search/", headers=headers, json=search_data)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["origin"] == search_data["origin"]
    assert data["destination"] == search_data["destination"]
    assert data["user_id"] == user.id


def test_get_search_history(test_app: TestClient, test_db: Session):
    """Test getting search history."""
    # Create a user
    user = create_random_user(test_db)
    
    # Get authentication headers
    headers = get_auth_headers(user.id)
    
    # Create multiple searches
    for _ in range(3):
        search_data = create_search_data(user.id)
        test_app.post("/api/v1/search/", headers=headers, json=search_data)
    
    # Make the request to get search history
    response = test_app.get("/api/v1/search/history", headers=headers)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["total"] >= 3
    assert len(data["items"]) >= 3
    assert all(item["user_id"] == user.id for item in data["items"])


def test_get_search_by_id(test_app: TestClient, test_db: Session):
    """Test getting a specific search by ID."""
    # Create a user
    user = create_random_user(test_db)
    
    # Get authentication headers
    headers = get_auth_headers(user.id)
    
    # Create a search first
    search_data = create_search_data(user.id)
    create_response = test_app.post("/api/v1/search/", headers=headers, json=search_data)
    search_id = create_response.json()["id"]
    
    # Make the request to get the search by ID
    response = test_app.get(f"/api/v1/search/{search_id}", headers=headers)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == search_id
    assert data["origin"] == search_data["origin"]
    assert data["destination"] == search_data["destination"]
    assert data["user_id"] == user.id


def test_search_flights(test_app: TestClient, test_db: Session):
    """Test searching for flights."""
    # Create a user
    user = create_random_user(test_db)
    
    # Get authentication headers
    headers = get_auth_headers(user.id)
    
    # Create search data
    search_data = create_search_data()
    
    # Make the request
    response = test_app.post("/api/v1/search/flights", headers=headers, json=search_data)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    # The response structure depends on your API implementation
    # This is a basic check that the endpoint responds successfully
    assert isinstance(data, dict)
    assert "success" in data

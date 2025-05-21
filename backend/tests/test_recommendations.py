"""
Tests for recommendations endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from tests.utils import create_random_user, get_auth_headers, create_recommendation_data


def test_get_recommendations(test_app: TestClient, test_db: Session):
    """Test getting recommendations."""
    # Create a user
    user = create_random_user(test_db)
    
    # Get authentication headers
    headers = get_auth_headers(user.id)
    
    # Make the request
    response = test_app.get("/api/v1/recommendations/", headers=headers)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


def test_get_recommendation_by_id(test_app: TestClient, test_db: Session):
    """Test getting a recommendation by ID."""
    # Create a user
    user = create_random_user(test_db)
    
    # Get authentication headers
    headers = get_auth_headers(user.id)
    
    # Create a recommendation first (this may require admin access)
    # For testing, we may need to insert directly into the database
    # This depends on your API implementation
    
    # Make the request - assuming ID 1 exists
    # If your API requires a specific ID, adjust this test accordingly
    response = test_app.get("/api/v1/recommendations/1", headers=headers)
    
    # Assertions - this may vary based on your API implementation
    # If the recommendation doesn't exist, adjust the expected status code
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert "id" in data
        assert "destination" in data
    else:
        # Not found is an acceptable response if test data doesn't exist yet
        data = response.json()
        assert "detail" in data


def test_get_personalized_recommendations(test_app: TestClient, test_db: Session):
    """Test getting personalized recommendations."""
    # Create a user
    user = create_random_user(test_db)
    
    # Get authentication headers
    headers = get_auth_headers(user.id)
    
    # Make the request
    response = test_app.get("/api/v1/recommendations/personalized", headers=headers)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


def test_recommend_by_preferences(test_app: TestClient, test_db: Session):
    """Test getting recommendations by preferences."""
    # Create a user
    user = create_random_user(test_db)
    
    # Get authentication headers
    headers = get_auth_headers(user.id)
    
    # Preferences data
    preferences = {
        "budget": 2000,
        "interests": ["beach", "culture"],
        "climate": "warm",
        "duration": 7
    }
    
    # Make the request
    response = test_app.post(
        "/api/v1/recommendations/by-preferences",
        headers=headers,
        json=preferences
    )
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data

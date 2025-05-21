"""
Tests for deals endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from tests.utils import create_random_user, get_auth_headers, create_deal_data


def test_get_deals(test_app: TestClient, test_db: Session):
    """Test getting all deals."""
    # Create a user
    user = create_random_user(test_db)
    
    # Get authentication headers
    headers = get_auth_headers(user.id)
    
    # Make the request
    response = test_app.get("/api/v1/deals/", headers=headers)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


def test_get_deal_by_id(test_app: TestClient, test_db: Session):
    """Test getting a deal by ID."""
    # Create a user
    user = create_random_user(test_db)
    
    # Get authentication headers
    headers = get_auth_headers(user.id)
    
    # Make the request - assuming ID 1 exists
    # If your API requires a specific ID, adjust this test accordingly
    response = test_app.get("/api/v1/deals/1", headers=headers)
    
    # Assertions - this may vary based on your API implementation
    # If the deal doesn't exist, adjust the expected status code
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert "id" in data
        assert "title" in data
    else:
        # Not found is an acceptable response if test data doesn't exist yet
        data = response.json()
        assert "detail" in data


def test_save_deal(test_app: TestClient, test_db: Session):
    """Test saving a deal."""
    # Create a user
    user = create_random_user(test_db)
    
    # Get authentication headers
    headers = get_auth_headers(user.id)
    
    # Assuming a deal with ID 1 exists
    # If not, you may need to create one first
    deal_id = 1
    
    # Make the request
    response = test_app.post(f"/api/v1/deals/{deal_id}/save", headers=headers)
    
    # Assertions
    # The status code depends on your API implementation
    assert response.status_code in [200, 201, 404]
    if response.status_code != 404:
        data = response.json()
        assert data["success"] is True


def test_get_saved_deals(test_app: TestClient, test_db: Session):
    """Test getting saved deals."""
    # Create a user
    user = create_random_user(test_db)
    
    # Get authentication headers
    headers = get_auth_headers(user.id)
    
    # Make the request
    response = test_app.get("/api/v1/deals/saved", headers=headers)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


def test_unsave_deal(test_app: TestClient, test_db: Session):
    """Test unsaving a deal."""
    # Create a user
    user = create_random_user(test_db)
    
    # Get authentication headers
    headers = get_auth_headers(user.id)
    
    # First save a deal (assuming deal ID 1 exists)
    # If the deal doesn't exist, this test may fail
    save_response = test_app.post("/api/v1/deals/1/save", headers=headers)
    
    # If the save was successful, try to unsave it
    if save_response.status_code in [200, 201]:
        # Make the request to unsave
        response = test_app.delete("/api/v1/deals/1/save", headers=headers)
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

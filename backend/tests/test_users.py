"""
Tests for user endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.schemas.user import UserCreate
from app.core.security import create_access_token


def get_token_headers(user_id: int) -> dict:
    """Helper to create authentication headers."""
    access_token = create_access_token(user_id)
    return {"Authorization": f"Bearer {access_token}"}


def create_test_user(db: Session, is_superuser: bool = False) -> dict:
    """Helper to create a test user."""
    user_data = {
        "email": f"user_{pytest.get_random_string()}@example.com",
        "password": "testpassword123",
        "full_name": "Test User",
        "is_superuser": is_superuser,
    }
    user_in = UserCreate(**user_data)
    user = crud.user.create(db=db, obj_in=user_in)
    return {"user": user, "data": user_data}


def test_read_user_me(test_app: TestClient, test_db: Session):
    """Test reading user profile."""
    # Create a test user
    user_info = create_test_user(test_db)
    user = user_info["user"]
    
    # Get authentication headers
    headers = get_token_headers(user.id)
    
    # Make the request
    response = test_app.get("/api/v1/users/me", headers=headers)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user.email
    assert data["full_name"] == user.full_name
    assert data["id"] == user.id


def test_update_user_me(test_app: TestClient, test_db: Session):
    """Test updating user profile."""
    # Create a test user
    user_info = create_test_user(test_db)
    user = user_info["user"]
    
    # Get authentication headers
    headers = get_token_headers(user.id)
    
    # Update data
    update_data = {
        "full_name": "Updated Name"
    }
    
    # Make the request
    response = test_app.patch("/api/v1/users/me", headers=headers, json=update_data)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == update_data["full_name"]
    assert data["email"] == user.email
    assert data["id"] == user.id


def test_read_users_superuser(test_app: TestClient, test_db: Session):
    """Test reading all users (superuser access)."""
    # Create a superuser
    superuser_info = create_test_user(test_db, is_superuser=True)
    superuser = superuser_info["user"]
    
    # Get authentication headers for superuser
    headers = get_token_headers(superuser.id)
    
    # Make the request
    response = test_app.get("/api/v1/users/", headers=headers)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_read_users_normal_user(test_app: TestClient, test_db: Session):
    """Test reading all users (normal user - should fail)."""
    # Create a normal user
    user_info = create_test_user(test_db)
    user = user_info["user"]
    
    # Get authentication headers
    headers = get_token_headers(user.id)
    
    # Make the request
    response = test_app.get("/api/v1/users/", headers=headers)
    
    # Assertions - should fail for normal users
    assert response.status_code == 403


def test_create_user_superuser(test_app: TestClient, test_db: Session):
    """Test creating a new user by superuser."""
    # Create a superuser
    superuser_info = create_test_user(test_db, is_superuser=True)
    superuser = superuser_info["user"]
    
    # Get authentication headers for superuser
    headers = get_token_headers(superuser.id)
    
    # New user data
    new_user_data = {
        "email": "new_user@example.com",
        "password": "newpassword123",
        "full_name": "New Test User",
    }
    
    # Make the request
    response = test_app.post("/api/v1/users/", headers=headers, json=new_user_data)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == new_user_data["email"]
    assert data["full_name"] == new_user_data["full_name"]

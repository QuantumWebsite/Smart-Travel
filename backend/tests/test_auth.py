"""
Tests for authentication endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.schemas.user import UserCreate


def test_register_user(test_app: TestClient, test_db: Session):
    """Test user registration endpoint."""
    # Test data
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    # Make the request
    response = test_app.post("/api/v1/auth/register", json=user_data)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data
    assert "password" not in data  # Password should not be returned
    assert "hashed_password" not in data  # Hashed password should not be returned


def test_login_user(test_app: TestClient, test_db: Session):
    """Test user login endpoint."""
    # Test data
    user_data = {
        "email": "login_test@example.com",
        "password": "testpassword123",
        "full_name": "Login Test User"
    }
    
    # Create a user first
    user_in = UserCreate(**user_data)
    crud.user.create(db=test_db, obj_in=user_in)
    
    # Login form data
    login_data = {
        "username": user_data["email"],  # OAuth2 uses username field for email
        "password": user_data["password"],
    }
    
    # Make the request
    response = test_app.post("/api/v1/auth/login/access-token", data=login_data)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_existing_user(test_app: TestClient, test_db: Session):
    """Test registering with an email that already exists."""
    # Test data
    user_data = {
        "email": "existing@example.com",
        "password": "testpassword123",
        "full_name": "Existing User"
    }
    
    # Create a user first
    user_in = UserCreate(**user_data)
    crud.user.create(db=test_db, obj_in=user_in)
    
    # Try to register the same email again
    response = test_app.post("/api/v1/auth/register", json=user_data)
    
    # Assertions
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data  # Should contain an error message


def test_login_wrong_password(test_app: TestClient, test_db: Session):
    """Test login with wrong password."""
    # Test data
    user_data = {
        "email": "wrong_password@example.com",
        "password": "testpassword123",
        "full_name": "Wrong Password User"
    }
    
    # Create a user first
    user_in = UserCreate(**user_data)
    crud.user.create(db=test_db, obj_in=user_in)
    
    # Login form data with wrong password
    login_data = {
        "username": user_data["email"],
        "password": "wrongpassword",
    }
    
    # Make the request
    response = test_app.post("/api/v1/auth/login/access-token", data=login_data)
    
    # Assertions
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data  # Should contain an error message

"""
Test email verification endpoints.
"""
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest
from datetime import datetime, timezone, timedelta

from app.core.security import generate_verification_token, create_verification_token_expiry
from app.models.user import User
from app.crud.user import user as crud_user


def test_verify_email_valid_token(test_app: TestClient, test_db: Session):
    """Test verifying email with a valid token."""
    # Create a test user with verification token
    verification_token = generate_verification_token()
    verification_token_expires = create_verification_token_expiry()
    
    user_data = {
        "email": "verify_test@example.com",
        "hashed_password": "hashedpassword",
        "full_name": "Verify Test",
        "is_active": False,
        "email_verified": False,
        "verification_token": verification_token,
        "verification_token_expires": verification_token_expires
    }
    
    user = User(**user_data)
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    
    # Test verification endpoint
    response = test_app.get(f"/api/v1/auth/verify-email/{verification_token}")
    
    assert response.status_code == 200
    assert response.json()["message"] == "Email verified successfully. You can now log in."
      # Check that the user is now verified in the database
    # First, expire all objects in session to clear the cache
    test_db.expire_all()
    # Then query for the user again to get fresh data
    updated_user = test_db.query(User).filter(User.email == "verify_test@example.com").first()
    assert updated_user.email_verified is True
    assert updated_user.is_active is True
    assert updated_user.verification_token is None
    assert updated_user.verification_token_expires is None
    
    # Clean up
    test_db.delete(updated_user)
    test_db.commit()


def test_verify_email_expired_token(test_app: TestClient, test_db: Session):
    """Test verifying email with an expired token."""
    # Create a test user with expired verification token
    verification_token = generate_verification_token()
    # Set expiration to yesterday
    expired_token_time = datetime.now(timezone.utc) - timedelta(days=1)
    
    user_data = {
        "email": "expired_token_test@example.com",
        "hashed_password": "hashedpassword",
        "full_name": "Expired Token Test",
        "is_active": False,
        "email_verified": False,
        "verification_token": verification_token,
        "verification_token_expires": expired_token_time
    }
    
    user = User(**user_data)
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    
    # Test verification endpoint with expired token
    response = test_app.get(f"/api/v1/auth/verify-email/{verification_token}")
    
    assert response.status_code == 400
    assert "expired" in response.json()["detail"].lower()
    
    # Clean up
    test_db.delete(user)
    test_db.commit()


def test_resend_verification(test_app: TestClient, test_db: Session):
    """Test resending verification email."""
    # Create a test user
    user_data = {
        "email": "resend_test@example.com",
        "hashed_password": "hashedpassword",
        "full_name": "Resend Test",
        "is_active": False,
        "email_verified": False,
        "verification_token": "old_token",
        "verification_token_expires": datetime.now(timezone.utc)
    }
    
    user = User(**user_data)
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    
    # Test resend verification endpoint
    response = test_app.post("/api/v1/auth/resend-verification", json={"email": "resend_test@example.com"})
    
    assert response.status_code == 200
    assert response.json()["message"] == "Verification email sent."
      # Check that the user's verification token has been updated
    # First, expire all objects in session to clear the cache
    test_db.expire_all()
    # Then query for the user again to get fresh data
    updated_user = test_db.query(User).filter(User.email == "resend_test@example.com").first()
    assert updated_user.verification_token != "old_token"
    
    # Ensure token_expires is timezone aware for comparison
    token_expires = updated_user.verification_token_expires
    if token_expires.tzinfo is None:
        # If naive datetime, assume UTC
        token_expires = token_expires.replace(tzinfo=timezone.utc)
    
    assert token_expires > datetime.now(timezone.utc)
    
    # Clean up
    test_db.delete(updated_user)
    test_db.commit()

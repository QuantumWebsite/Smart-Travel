"""
Test the full email verification flow from registration through verification.
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch, MagicMock

from app.models.user import User
from app.services.email.email_service import EmailService


@pytest.fixture
def mock_email_service():
    """
    Mock the email service for testing
    
    In normal test environments: Mock the email service
    With MailDev: If MAILDEV_TESTING=True env var is set, actually send the email
    """
    # Check if we're using MailDev for testing
    use_maildev = os.environ.get("MAILDEV_TESTING", "").lower() == "true"
    
    if use_maildev:
        # Don't mock, let it use the real MailDev service
        # But return a callable mock to track calls for assertions
        mock = MagicMock(return_value=True)
        yield mock
    else:
        # Normal test mode - mock the email service
        with patch.object(EmailService, 'send_email', return_value=True) as mock:
            yield mock


def test_full_verification_flow(test_app: TestClient, test_db: Session, mock_email_service):
    """
    Test the full user registration and email verification flow:
    1. Register a new user
    2. Check that verification email would be sent
    3. Check that user is inactive and not verified
    4. Use the verification token to verify the account
    5. Check that the user is now active and verified
    6. Try to login before verification (should fail)
    7. Try to login after verification (should succeed)
    """    # Step 1: Register a new user
    user_data = {
        "email": "verify_flow_test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    registration_response = test_app.post("/api/v1/auth/register", json=user_data)
    assert registration_response.status_code == 200
    assert registration_response.json()["email"] == user_data["email"]
    assert registration_response.json()["email_verified"] is False
    assert registration_response.json()["is_active"] is False
    
    # Step 2: Check that verification email would be sent
    mock_email_service.assert_called_once()
    
    # Step 3: Check that user is inactive and not verified in the database
    user = test_db.query(User).filter(User.email == user_data["email"]).first()
    assert user is not None
    assert user.email_verified is False
    assert user.is_active is False
    assert user.verification_token is not None
    assert user.verification_token_expires is not None
    
    # Save the verification token
    verification_token = user.verification_token
    
    # Step 4: Try to login before verification (should fail)
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    login_response = test_app.post("/api/v1/auth/login/access-token", data=login_data)
    assert login_response.status_code == 400
    assert "email not verified" in login_response.json()["detail"].lower()
    
    # Step 5: Use the verification token to verify the account
    verification_response = test_app.get(f"/api/v1/auth/verify-email/{verification_token}")
    assert verification_response.status_code == 200
    assert verification_response.json()["message"] == "Email verified successfully. You can now log in."
      # Step 6: Check that the user is now active and verified in the database
    # First, expire all objects in session to clear the cache
    test_db.expire_all()
    # Then query for the user again to get fresh data
    user = test_db.query(User).filter(User.email == user_data["email"]).first()
    assert user.email_verified is True
    assert user.is_active is True
    assert user.verification_token is None
    assert user.verification_token_expires is None
    
    # Step 7: Try to login after verification (should succeed)
    login_response = test_app.post("/api/v1/auth/login/access-token", data=login_data)
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    
    # Clean up
    test_db.delete(user)
    test_db.commit()


def test_resend_verification(test_app: TestClient, test_db: Session, mock_email_service):
    """
    Test the flow for resending a verification email:
    1. Register a new user
    2. Check initial verification token
    3. Request a new verification email
    4. Check that the verification token has changed
    5. Verify using the new token
    """
    # Step 1: Register a new user
    user_data = {
        "email": "resend_flow_test@example.com",
        "password": "testpassword123",
        "full_name": "Resend Test User"
    }
    
    registration_response = test_app.post("/api/v1/auth/register", json=user_data)
    assert registration_response.status_code == 200
    
    # Get the original verification token
    user = test_db.query(User).filter(User.email == user_data["email"]).first()
    original_token = user.verification_token
    
    # Reset the mock to check for the resend call
    mock_email_service.reset_mock()
    
    # Step 2: Request a new verification email
    resend_response = test_app.post("/api/v1/auth/resend-verification", 
                                  json={"email": user_data["email"]})
    assert resend_response.status_code == 200
    assert resend_response.json()["message"] == "Verification email sent."
    
    # Check that the email service was called    mock_email_service.assert_called_once()
    
    # Step 3: Check that the verification token has changed
    # First, expire all objects in session to clear the cache
    test_db.expire_all()
    # Then query for the user again to get the fresh data
    user = test_db.query(User).filter(User.email == user_data["email"]).first()
    assert user.verification_token != original_token
    assert user.verification_token is not None
    
    # Step 4: Verify using the new token
    new_token = user.verification_token
    verification_response = test_app.get(f"/api/v1/auth/verify-email/{new_token}")
    assert verification_response.status_code == 200
      # Step 5: Check that the user is now verified
    # Expire all objects in session to clear the cache
    test_db.expire_all()
    # Query for the user again to get fresh data
    user = test_db.query(User).filter(User.email == user_data["email"]).first()
    assert user.email_verified is True
    assert user.is_active is True
    
    # Clean up
    test_db.delete(user)
    test_db.commit()


def test_expired_verification_token(test_app: TestClient, test_db: Session, mock_email_service):
    """
    Test the handling of expired verification tokens:
    1. Create a user with an expired token
    2. Try to verify with the expired token (should fail)
    3. Request a new token
    4. Verify with the new token (should succeed)
    """
    import datetime
    
    # Step 1: Create a user with an expired token
    expired_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    expired_token = "expired_token_123"
    
    user_data = {
        "email": "expired_token@example.com",
        "hashed_password": "hashedpassword",
        "full_name": "Expired Token User",
        "is_active": False,
        "email_verified": False,
        "verification_token": expired_token,
        "verification_token_expires": expired_time
    }
    
    user = User(**user_data)
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    
    # Step 2: Try to verify with the expired token
    verification_response = test_app.get(f"/api/v1/auth/verify-email/{expired_token}")
    assert verification_response.status_code == 400
    assert "expired" in verification_response.json()["detail"].lower()
    
    # Step 3: Request a new token
    mock_email_service.reset_mock()
    resend_response = test_app.post("/api/v1/auth/resend-verification", 
                                  json={"email": user_data["email"]})
    assert resend_response.status_code == 200
      # Step 4: Get the new token and verify with it
    # First, expire all objects in session to clear the cache
    test_db.expire_all()
    # Then query for the user again to get fresh data
    user = test_db.query(User).filter(User.email == user_data["email"]).first()
    new_token = user.verification_token
    assert new_token != expired_token
    
    verification_response = test_app.get(f"/api/v1/auth/verify-email/{new_token}")
    assert verification_response.status_code == 200
      # Check that the user is now verified
    # First, expire all objects in session to clear the cache
    test_db.expire_all()
    # Then query for the user again to get fresh data
    user = test_db.query(User).filter(User.email == user_data["email"]).first()
    assert user.email_verified is True
    assert user.is_active is True
    
    # Clean up
    test_db.delete(user)
    test_db.commit()

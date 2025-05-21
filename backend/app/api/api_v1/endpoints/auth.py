from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import datetime

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.core import security
from app.core.security import get_password_hash
from datetime import timedelta
from app.services.email import email_service

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.email_verified:
        raise HTTPException(status_code=400, detail="Email not verified. Please check your email to verify your account.")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/register", response_model=schemas.User)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
):
    """
    Register a new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists."
        )
      # Create a verification token
    verification_token = security.generate_verification_token()
    verification_token_expires = security.create_verification_token_expiry()
    
    # Create user with verification data
    user = crud.user.create_with_verification(
        db,
        obj_in=user_in,
        verification_token=verification_token,
        token_expires=verification_token_expires
    )
      # Send verification email
    email_service.send_verification_email(user.email, verification_token)
    
    return user


@router.post("/password-recovery/{email}", response_model=schemas.Message)
def recover_password(email: str, db: Session = Depends(deps.get_db)):
    """
    Password Recovery
    """
    user = crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    
    # TODO
    # In a real application, would send a password recovery email here
    # For now, just return a message
    
    return {"message": "Password recovery email sent"}


@router.post("/reset-password", response_model=schemas.Message)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
):
    """
    Reset password using a recovery token
    """
    # TODO: Implement password reset logic
    
    return {"message": "Password updated successfully"}
    """
    Reset password
    """
    # TODO
    # In a real application, would validate the token and update the password
    # For now, just return a message
    
    return {"message": "Password updated successfully"}


@router.get("/verify-email/{token}", response_model=schemas.Message)
def verify_email(
    token: str,
    db: Session = Depends(deps.get_db),
):
    """
    Verify user email with token
    """
    user = crud.user.get_by_verification_token(db, token=token)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The verification token is invalid."
        )
      # Check if token is expired
    # Ensure token expiry has timezone info before comparison
    token_expires = user.verification_token_expires
    if token_expires.tzinfo is None:
        # If naive datetime, assume UTC
        token_expires = token_expires.replace(tzinfo=datetime.timezone.utc)
        
    if token_expires < datetime.datetime.now(datetime.timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="The verification token has expired."
        )
    
    # Verify the user's email
    crud.user.verify_email(db, user=user)
    
    return {"message": "Email verified successfully. You can now log in."}


@router.post("/resend-verification", response_model=schemas.Message)
def resend_verification_email(
    email_data: dict = Body(...),
    db: Session = Depends(deps.get_db),
):
    """
    Resend verification email to user
    
    Request body should be JSON: {"email": "user@example.com"}
    """
    email = email_data.get("email")
    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email is required in the request body."
        )
        
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system."
        )
    
    if user.email_verified:
        raise HTTPException(
            status_code=400,
            detail="Email already verified."
        )
    # Create a new verification token - ensure it's different from the current one
    verification_token = security.generate_verification_token()
    while verification_token == user.verification_token:
        verification_token = security.generate_verification_token()
        
    verification_token_expires = security.create_verification_token_expiry()
    
    # Update user with new verification data
    crud.user.update_verification_token(
        db,
        user=user,
        verification_token=verification_token,
        token_expires=verification_token_expires
    )
      # Send verification email
    email_service.send_verification_email(user.email, verification_token)
    
    return {"message": "Verification email sent."}

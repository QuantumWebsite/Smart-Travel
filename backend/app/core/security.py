from typing import Any, Dict, Optional, Union
import datetime
import secrets

from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = settings.JWT_ALGORITHM


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[datetime.timedelta] = None
) -> str:
    """
    Create access token with specified subject and expiration
    
    Args:
        subject: Subject/user ID for the token
        expires_delta: Optional expiration time delta
        
    Returns:
        Encoded JWT token
    """
    
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that plain password matches hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password with bcrypt
    """
    return pwd_context.hash(password)


def generate_verification_token() -> str:
    """
    Generate a secure random token for email verification
    
    Returns:
        A URL-safe random token
    """
    return secrets.token_urlsafe(32)


def create_verification_token_expiry() -> datetime.datetime:
    """
    Create expiration timestamp for verification tokens
    
    Returns:
        Timestamp 24 hours in the future
    """
    return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    
    
# These functions are already defined above - removed duplicate implementations

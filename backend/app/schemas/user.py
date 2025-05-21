from typing import Optional
from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    """API message response schema"""
    message: str


class UserBase(BaseModel):
    """Base user schema"""
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = False  # Changed default to False until email is verified
    is_superuser: bool = False
    full_name: Optional[str] = None
    email_verified: Optional[bool] = False


class UserCreate(UserBase):
    """Schema for user creation"""
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    """Schema for user update"""
    password: Optional[str] = None


class UserInDBBase(UserBase):
    """Base user schema with DB fields"""
    id: Optional[int] = None
    
    model_config = {
        "from_attributes": True
    }


class User(UserInDBBase):
    """API schema for user data"""
    pass


class UserInDB(UserInDBBase):
    """Schema for user in DB with hashed password"""
    hashed_password: str
    email_verified: Optional[bool] = False

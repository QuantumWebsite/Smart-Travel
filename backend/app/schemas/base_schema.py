from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from pydantic import BaseModel


class Message(BaseModel):
    """
    Basic message response schema
    """
    success: bool = True
    message: str


class ErrorResponse(BaseModel):
    """
    Error response schema
    """
    success: bool = False
    error: str
    detail: Optional[Dict[str, Any]] = None


T = TypeVar('T')


class DefaultCreate(BaseModel):
    """
    Default create schema with empty implementation
    Used as a placeholder for CRUD operations that don't have a specific create schema
    """
    pass


class DefaultUpdate(BaseModel):
    """
    Default update schema with empty implementation
    Used as a placeholder for CRUD operations that don't have a specific update schema
    """
    pass


class ResponseList(BaseModel, Generic[T]):
    """
    Paginated response list schema
    """
    success: bool = True
    total: int
    items: List[T]

from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """
    Token schema
    """
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    Token payload schema for JWT
    """
    sub: Optional[int] = None
    exp: Optional[int] = None

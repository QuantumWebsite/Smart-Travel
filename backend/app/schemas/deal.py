from typing import Optional, Dict, Any
from pydantic import BaseModel
import datetime


class SavedDealBase(BaseModel):
    """Base saved deal schema"""
    user_id: int
    search_id: Optional[int] = None
    type: str  # 'flight', 'hotel', 'package', etc.
    provider: str
    title: str
    description: Optional[str] = None
    price: float
    currency: str = "USD"
    url: str
    details: Dict[str, Any] = {}
    image_url: Optional[str] = None


class SavedDealCreate(SavedDealBase):
    """Schema for saved deal creation"""
    pass


class SavedDealUpdate(BaseModel):
    """Schema for saved deal update"""
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    url: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    image_url: Optional[str] = None


class SavedDeal(SavedDealBase):
    """API schema for saved deal data"""
    id: int
    created_at: datetime.datetime
    
    model_config = {
        "from_attributes": True
    }

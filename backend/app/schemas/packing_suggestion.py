from typing import Optional, List
from pydantic import BaseModel
import datetime


class PackingSuggestionBase(BaseModel):
    """Base packing suggestion schema"""
    search_id: int
    category: str  # 'clothing', 'toiletries', 'documents', 'electronics', etc.
    item_name: str
    quantity: int = 1
    importance: str = "medium"  # 'low', 'medium', 'high'
    notes: Optional[str] = None


class PackingSuggestionCreate(PackingSuggestionBase):
    """Schema for packing suggestion creation"""
    pass


class PackingSuggestionUpdate(BaseModel):
    """Schema for packing suggestion update"""
    category: Optional[str] = None
    item_name: Optional[str] = None
    quantity: Optional[int] = None
    importance: Optional[str] = None
    notes: Optional[str] = None


class PackingSuggestion(PackingSuggestionBase):
    """API schema for packing suggestion data"""
    id: int
    created_at: datetime.datetime
    
    model_config = {
        "from_attributes": True
    }

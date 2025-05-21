from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from datetime import datetime


class RecommendationBase(BaseModel):
    """Base recommendation schema"""
    search_id: int
    type: str  # 'destination', 'flight', 'hotel', 'activity', etc.
    title: str
    description: str
    score: float
    details: Dict[str, Any] = {}
    image_url: Optional[str] = None


class RecommendationCreate(RecommendationBase):
    """Schema for recommendation creation"""
    pass


class RecommendationUpdate(BaseModel):
    """Schema for recommendation update"""
    title: Optional[str] = None
    description: Optional[str] = None
    score: Optional[float] = None
    details: Optional[Dict[str, Any]] = None
    image_url: Optional[str] = None


class Recommendation(RecommendationBase):
    """API schema for recommendation data"""
    id: int
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }

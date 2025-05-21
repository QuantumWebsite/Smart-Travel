from typing import Optional, Dict, Any, List
from datetime import date
from pydantic import BaseModel, Field


class SearchBase(BaseModel):
    destination: str
    departure_location: str
    departure_date: date
    return_date: date
    adults: int = 1
    children: int = 0
    budget: Optional[float] = None
    preferences: Optional[Dict[str, Any]] = None


class SearchCreate(SearchBase):
    user_id: Optional[int] = None


class SearchUpdate(SearchBase):
    destination: Optional[str] = None
    departure_location: Optional[str] = None
    departure_date: Optional[date] = None
    return_date: Optional[date] = None


class SearchInDBBase(SearchBase):
    id: int
    user_id: Optional[int]
    status: str = "processing"  # processing, completed, failed
    error_message: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class Search(SearchInDBBase):
    pass


class SearchWithResults(Search):
    flights: Optional[List[Any]] = None
    hotels: Optional[List[Any]] = None
    weather: Optional[Dict[str, Any]] = None
    events: Optional[List[Any]] = None
    
    
class SearchResponse(BaseModel):
    """Response model for search API endpoints"""
    search_id: Optional[int] = None
    status: Optional[str] = None
    message: Optional[str] = None
    
    # For responses that include full search data
    search: Optional[Search] = None
    flights: Optional[List[Any]] = None
    hotels: Optional[List[Any]] = None
    weather_data: Optional[List[Any]] = None
    events: Optional[List[Any]] = None
    recommendations: Optional[List[Any]] = None
    data: Optional[Dict[str, Any]] = None
    search: Optional[Search] = None
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, JSON, Text
from sqlalchemy.orm import relationship
import datetime

from app.db.base_class import Base


class Recommendation(Base):
    id = Column(Integer, primary_key=True, index=True)
    search_id = Column(Integer, ForeignKey("search.id"))
    flight_id = Column(Integer, ForeignKey("flight.id"), nullable=True)
    hotel_id = Column(Integer, ForeignKey("hotel.id"), nullable=True)
    score = Column(Float)  # Recommendation score (higher is better)
    price_score = Column(Float, nullable=True)  # Component scores
    weather_score = Column(Float, nullable=True)
    convenience_score = Column(Float, nullable=True)
    summary = Column(Text)  # AI-generated summary of why this is recommended
    details = Column(JSON, nullable=True)  # Additional recommendation details
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    # Relationships
    search = relationship("Search", back_populates="recommendations")
    flight = relationship("Flight")
    hotel = relationship("Hotel")
    
    # Packing suggestions relation (optional)
    packing_suggestions = relationship("PackingSuggestion", back_populates="recommendation")
    notifications = relationship("Notification", back_populates="recommendation")

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Float, Boolean
from sqlalchemy.orm import relationship
import datetime

from app.db.base_class import Base


class Search(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    destination = Column(String, nullable=False)
    departure_location = Column(String, nullable=False)
    departure_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=False)
    adults = Column(Integer, default=1)
    children = Column(Integer, default=0)
    budget = Column(Float, nullable=True)
    preferences = Column(JSON, nullable=True)  # Store user preferences like weather, activities, etc.   
    status = Column(String, default="processing")  # processing, completed, failed
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="searches")
    flights = relationship("Flight", back_populates="search")
    hotels = relationship("Hotel", back_populates="search")
    weather_data = relationship("Weather", back_populates="search")
    events = relationship("Event", back_populates="search")
    recommendations = relationship("Recommendation", back_populates="search")

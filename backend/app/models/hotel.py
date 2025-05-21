from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, JSON, Text
from sqlalchemy.orm import relationship
import datetime

from app.db.base_class import Base


class Hotel(Base):
    id = Column(Integer, primary_key=True, index=True)
    search_id = Column(Integer, ForeignKey("search.id"))
    name = Column(String)
    location = Column(String)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    price_per_night = Column(Float)
    currency = Column(String, default="USD")
    rating = Column(Float, nullable=True)
    amenities = Column(JSON, nullable=True)
    description = Column(Text, nullable=True)
    source_website = Column(String)  # Booking.com, Airbnb
    source_url = Column(String)
    image_url = Column(String, nullable=True)
    details = Column(JSON, nullable=True)  # Additional hotel details
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    # Relationships
    search = relationship("Search", back_populates="hotels")

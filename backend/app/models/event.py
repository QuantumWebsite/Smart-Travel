from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, JSON, Text, Boolean
from sqlalchemy.orm import relationship
import datetime

from app.db.base_class import Base


class Event(Base):
    id = Column(Integer, primary_key=True, index=True)
    search_id = Column(Integer, ForeignKey("search.id"))
    title = Column(String)
    description = Column(Text, nullable=True)
    location = Column(String)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime, nullable=True)
    price = Column(Float, nullable=True)
    currency = Column(String, default="USD")
    is_free = Column(Boolean, default=False)
    category = Column(String, nullable=True)
    source_website = Column(String)  # Eventbrite, Meetup
    source_url = Column(String)
    image_url = Column(String, nullable=True)
    details = Column(JSON, nullable=True)  # Additional event details
    created_at = Column(DateTime, default= (datetime.timezone.utc))
    
    # Relationships
    search = relationship("Search", back_populates="events")

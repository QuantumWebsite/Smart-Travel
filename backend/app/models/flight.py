from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, JSON, Text
from sqlalchemy.orm import relationship
import datetime

from app.db.base_class import Base


class Flight(Base):
    id = Column(Integer, primary_key=True, index=True)
    search_id = Column(Integer, ForeignKey("search.id"))
    airline = Column(String)
    flight_number = Column(String)
    origin = Column(String)
    destination = Column(String)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    duration_minutes = Column(Integer)
    price = Column(Float)
    currency = Column(String, default="USD")
    layovers = Column(Integer, default=0)
    source_website = Column(String)  # Skyscanner, Google Flights, Expedia
    source_url = Column(String)
    details = Column(JSON, nullable=True)  # Additional flight details
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    # Relationships
    search = relationship("Search", back_populates="flights")

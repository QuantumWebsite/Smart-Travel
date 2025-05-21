from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, JSON
from sqlalchemy.orm import relationship
import datetime

from app.db.base_class import Base


class Weather(Base):
    id = Column(Integer, primary_key=True, index=True)
    search_id = Column(Integer, ForeignKey("search.id"))
    location = Column(String)
    date = Column(DateTime)
    temperature_high = Column(Float)
    temperature_low = Column(Float)
    condition = Column(String)  # Sunny, Cloudy, Rainy, etc.
    precipitation_chance = Column(Float)  # Percentage
    humidity = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    source_website = Column(String)  # Weather.com, AccuWeather
    details = Column(JSON, nullable=True)  # Additional weather details
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    # Relationships
    search = relationship("Search", back_populates="weather_data")

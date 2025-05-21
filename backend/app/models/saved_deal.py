from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Text
from sqlalchemy.orm import relationship
import datetime

from app.db.base_class import Base


class SavedDeal(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    recommendation_id = Column(Integer, ForeignKey("recommendation.id"))
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    # Relationships
    user = relationship("User", back_populates="saved_deals")
    recommendation = relationship("Recommendation")

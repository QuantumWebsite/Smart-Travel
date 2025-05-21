from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
import datetime

from app.db.base_class import Base


class PackingSuggestion(Base):
    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(Integer, ForeignKey("recommendation.id"))
    category = Column(String)  # clothing, accessories, documents, etc.
    items = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    # Relationships
    recommendation = relationship("Recommendation", back_populates="packing_suggestions")

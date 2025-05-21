from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
import datetime

from app.db.base_class import Base


class Notification(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    title = Column(String)
    message = Column(Text)
    type = Column(String)  # price_alert, weather_alert, deal_alert
    recommendation_id = Column(Integer, ForeignKey("recommendation.id"), nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    # Relationships
    user = relationship("User", back_populates="notifications")
    recommendation = relationship("Recommendation", back_populates="notifications")

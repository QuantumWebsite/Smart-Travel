from sqlalchemy import Boolean, Column, String, DateTime, Integer
from sqlalchemy.orm import relationship
import datetime

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean(), default=False)  # Changed to False by default until email is verified
    is_superuser = Column(Boolean(), default=False)
    email_verified = Column(Boolean(), default=False)
    verification_token = Column(String, nullable=True)
    verification_token_expires = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    
    # Relationships
    searches = relationship("Search", back_populates="user")
    saved_deals = relationship("SavedDeal", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

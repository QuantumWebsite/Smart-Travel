"""
Script to initialize the database schema for the Smart Travel API
"""
import os
import sys
from sqlalchemy import engine

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.base_class import Base
from app.db.session import engine
from app.models import __all_models  # This will import all model files
from app import crud
from app.core.config import settings

# Import all models to register them with SQLAlchemy
from app.models.user import User
from app.models.search import Search
from app.models.recommendation import Recommendation
from app.models.flight import Flight
from app.models.hotel import Hotel
from app.models.weather import Weather
from app.models.event import Event
from app.models.notification import Notification
from app.models.saved_deal import SavedDeal
from app.models.packing_suggestion import PackingSuggestion


def init_db() -> None:
    """Create database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")


if __name__ == "__main__":
    init_db()

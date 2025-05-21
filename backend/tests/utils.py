"""
Test helper utilities for generating test data.
"""
import random
from datetime import datetime, timedelta
import pytest
from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.user import UserCreate
from app.core.security import create_access_token


def get_random_string(length=10):
    """Generate a random string."""
    return pytest.get_random_string(length)


def get_random_email():
    """Generate a random email."""
    return f"test_{get_random_string()}@example.com"


def get_random_date(days_in_future=30):
    """Generate a random date in the future."""
    return (datetime.now() + timedelta(days=random.randint(1, days_in_future))).date()


def create_random_user(db: Session):
    """Create a random user."""
    email = get_random_email()
    password = get_random_string(12)
    user_in = UserCreate(
        email=email,
        password=password,
        full_name=f"Test User {get_random_string(5)}"
    )
    user = crud.user.create(db=db, obj_in=user_in)
    return user


def get_auth_headers(user_id: int):
    """Get authentication headers for a user."""
    access_token = create_access_token(user_id)
    return {"Authorization": f"Bearer {access_token}"}


def create_search_data(user_id: int = None):
    """Create random search data."""
    departure_date = get_random_date(10).isoformat()
    return_date = get_random_date(20).isoformat()
    
    return {
        "origin": random.choice(["NYC", "LAX", "CHI", "MIA", "SFO"]),
        "destination": random.choice(["LON", "PAR", "ROM", "TOK", "SYD"]),
        "departure_date": departure_date,
        "return_date": return_date,
        "adults": random.randint(1, 4),
        "children": random.randint(0, 2),
        "cabin_class": random.choice(["economy", "premium_economy", "business", "first"]),
        "preferences": {
            "max_price": random.randint(500, 2000),
            "max_stops": random.randint(0, 2),
            "preferred_airlines": []
        },
        "user_id": user_id
    }


def create_recommendation_data():
    """Create random recommendation test data."""
    return {
        "destination": random.choice(["London", "Paris", "Rome", "Tokyo", "Sydney"]),
        "description": f"Test recommendation for {get_random_string()}",
        "image_url": f"https://example.com/images/{get_random_string()}.jpg",
        "price_range": f"${random.randint(500, 2000)} - ${random.randint(2000, 5000)}",
        "best_time_to_visit": ["January", "February"] if random.random() > 0.5 else ["June", "July"],
        "tags": ["beach", "city", "culture"] if random.random() > 0.5 else ["mountains", "adventure", "relaxation"]
    }


def create_deal_data():
    """Create random deal test data."""
    return {
        "title": f"Special deal to {random.choice(['London', 'Paris', 'Rome', 'Tokyo', 'Sydney'])}",
        "description": f"Test deal description {get_random_string()}",
        "destination": random.choice(["London", "Paris", "Rome", "Tokyo", "Sydney"]),
        "price": random.randint(500, 2000),
        "discount_percent": random.randint(5, 30),
        "start_date": get_random_date(5).isoformat(),
        "end_date": get_random_date(15).isoformat(),
        "image_url": f"https://example.com/deals/{get_random_string()}.jpg",
        "link": f"https://example.com/deals/{get_random_string()}"
    }

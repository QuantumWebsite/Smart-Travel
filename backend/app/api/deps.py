from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from app.services.scraper.bright_data_client import BrightDataClient
from app.services.scraper import (
    get_bright_data_client, 
    get_flight_scraper,
    get_hotel_scraper,
    get_weather_scraper,
    get_event_scraper
)
from app.services.scraper.flight_scraper import FlightScraper
from app.services.scraper.hotel_scraper import HotelScraper
from app.services.scraper.weather_scraper import WeatherScraper
from app.services.scraper.event_scraper import EventScraper
from app.services.init_services import bright_data_client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token")


def get_db() -> Generator:
    """
    Dependency for getting database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Temporary simplified version for development
def get_current_user():
    """
    Get current user from token - simplified for development
    """
    # Return a mock user for development until auth is fully implemented
    class MockUser:
        id = 1
        email = "user@example.com"
        is_active = True
        is_superuser = False
        
    return MockUser()


# Temporary simplified version for development
def get_current_active_user():
    """
    Get current active user - simplified for development
    """
    return get_current_user()


# Temporary simplified version for development
def get_current_active_superuser():
    """
    Get current active superuser - simplified for development
    """
    user = get_current_user()
    if not user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


# Dependencies for Bright Data client and scrapers
def get_bright_data_client_dep() -> BrightDataClient:
    """
    Dependency for getting the global Bright Data client
    """
    if bright_data_client is None:
        raise HTTPException(
            status_code=500,
            detail="Bright Data client not initialized"
        )
    return bright_data_client


def get_flight_scraper_dep() -> FlightScraper:
    """
    Dependency for getting a FlightScraper instance
    """
    if bright_data_client is None:
        raise HTTPException(
            status_code=500,
            detail="Bright Data client not initialized"
        )
    return FlightScraper(bright_data_client=bright_data_client)


def get_hotel_scraper_dep() -> HotelScraper:
    """
    Dependency for getting a HotelScraper instance
    """
    if bright_data_client is None:
        raise HTTPException(
            status_code=500,
            detail="Bright Data client not initialized"
        )
    return HotelScraper(bright_data_client=bright_data_client)


def get_weather_scraper_dep() -> WeatherScraper:
    """
    Dependency for getting a WeatherScraper instance
    """
    if bright_data_client is None:
        raise HTTPException(
            status_code=500,
            detail="Bright Data client not initialized"
        )
    return WeatherScraper(bright_data_client=bright_data_client)


def get_event_scraper_dep() -> EventScraper:
    """
    Dependency for getting an EventScraper instance
    """
    if bright_data_client is None:
        raise HTTPException(
            status_code=500,
            detail="Bright Data client not initialized"
        )
    return EventScraper(bright_data_client=bright_data_client)

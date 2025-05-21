from app.services.scraper.bright_data_client import BrightDataClient
from app.services.scraper.base_scraper import BaseScraper
from app.services.scraper.flight_scraper import FlightScraper
from app.services.scraper.hotel_scraper import HotelScraper
from app.services.scraper.weather_scraper import WeatherScraper
from app.services.scraper.event_scraper import EventScraper
from app.core.config import settings


# Factory function to create a BrightDataClient instance
async def get_bright_data_client() -> BrightDataClient:
    """
    Factory function to create and configure a BrightDataClient instance
    
    Returns:
        Configured BrightDataClient instance
    """
    client = BrightDataClient(
        api_key=settings.BRIGHT_DATA_API_KEY,
        zone_name="mcp_unlocker",  # Default zone name, can be customized
        zone_username=settings.BRIGHT_DATA_ZONE_USERNAME,
        zone_password=settings.BRIGHT_DATA_ZONE_PASSWORD
    )
    return client


# Factory functions to create scraper instances with the BrightDataClient
async def get_flight_scraper() -> FlightScraper:
    """Get a FlightScraper instance with BrightDataClient"""
    client = await get_bright_data_client()
    return FlightScraper(bright_data_client=client)


async def get_hotel_scraper() -> HotelScraper:
    """Get a HotelScraper instance with BrightDataClient"""
    client = await get_bright_data_client()
    return HotelScraper(bright_data_client=client)


async def get_weather_scraper() -> WeatherScraper:
    """Get a WeatherScraper instance with BrightDataClient"""
    client = await get_bright_data_client()
    return WeatherScraper(bright_data_client=client)


async def get_event_scraper() -> EventScraper:
    """Get an EventScraper instance with BrightDataClient"""
    client = await get_bright_data_client()
    return EventScraper(bright_data_client=client)
import logging
from app.services.scraper.bright_data_client import BrightDataClient
from app.core.config import settings
import google.generativeai as genai

# Global instance of clients to be used throughout the app
logger = logging.getLogger(__name__)
bright_data_client = None

async def initialize_services():
    """
    Initialize services on application startup
    """
    global bright_data_client
    
    # Initialize Bright Data client
    bright_data_client = BrightDataClient(
        api_key=settings.BRIGHT_DATA_API_KEY,
        zone_name="mcp_unlocker",
        zone_username=settings.BRIGHT_DATA_ZONE_USERNAME,
        zone_password=settings.BRIGHT_DATA_ZONE_PASSWORD
    )
    
    # Initialize Gemini API if API key is provided
    if settings.GEMINI_API_KEY:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        logger.info("Initialized Gemini API client")
    
async def cleanup_services():
    """
    Clean up resources on application shutdown
    """
    global bright_data_client
    if bright_data_client:
        await bright_data_client.close()

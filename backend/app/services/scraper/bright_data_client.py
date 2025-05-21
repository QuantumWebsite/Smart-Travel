import logging
import json
import asyncio
from typing import Dict, Any, Optional, List
import aiohttp
from urllib.parse import quote_plus

from app.core.config import settings

logger = logging.getLogger(__name__)


class BrightDataClient:
    """
    Client for Bright Data Web Unlocker API and MCP Services
    
    This client provides methods to make requests to websites using Bright Data's 
    Web Unlocker API to bypass anti-scraping protections.
    
    The client supports both Direct API (RESTful) access which is recommended
    and also provides proxy-based access options as a fallback.
    """
    def __init__(self, api_key: str = None, zone_name: str = "mcp_unlocker", 
                 zone_username: str = None, zone_password: str = None):
        """
        Initialize the Bright Data client
        
        Args:
            api_key: Bright Data API key (if None, uses settings.BRIGHT_DATA_API_KEY)
            zone_name: The name of your Web Unlocker zone (default: mcp_unlocker)
            zone_username: Username for zone authentication (if None, uses settings.BRIGHT_DATA_ZONE_USERNAME)
            zone_password: Password for zone authentication (if None, uses settings.BRIGHT_DATA_ZONE_PASSWORD)
        """
        self.api_key = api_key or settings.BRIGHT_DATA_API_KEY
        self.zone_name = zone_name
        self.zone_username = zone_username or settings.BRIGHT_DATA_ZONE_USERNAME
        self.zone_password = zone_password or settings.BRIGHT_DATA_ZONE_PASSWORD
        self.api_base_url = "https://api.brightdata.com"
        self.session = None
        
        if not self.api_key:
            logger.warning("Bright Data API key not set. Client will operate in mock mode.")
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close(self):
        """Close the session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def request(self, 
                     url: str, 
                     method: str = "GET",
                     headers: Optional[Dict[str, str]] = None,
                     data: Optional[Dict[str, Any]] = None,
                     browser_emulation: bool = False,
                     data_format: str = "raw",
                     country_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Make a request to a website using Bright Data Web Unlocker API
        
        Args:
            url: The URL to request
            method: HTTP method (GET, POST, etc.)
            headers: Optional HTTP headers
            data: Optional data for POST requests
            browser_emulation: Whether to use browser emulation
            data_format: Format of the response data ('raw', 'markdown', 'json')
            country_code: Optional country code for geolocation
              Returns:
            Response data from the website
        """
        if not self.api_key:
            logger.info("Using mock data since API key is not set")
            return self._generate_mock_response(url)
        
        try:
            session = await self._get_session()            
            request_data = {
                "url": url,
                "zone": self.zone_name,
                "format": "raw",  # Return raw response
                "data_format": data_format
            }
            
            # Add zone authentication if credentials are provided
            if self.zone_username and self.zone_password:
                request_data["auth"] = {
                    "username": self.zone_username,
                    "password": self.zone_password
                }
            
            if browser_emulation:
                request_data["browser"] = True
                
            if method.upper() != "GET":
                request_data["method"] = method.upper()
                
            if headers:
                request_data["headers"] = headers
                
            if data:
                request_data["data"] = data
            
            if country_code:
                request_data["country"] = country_code
            
            # Make the request to Bright Data API
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # Add timeout to prevent hanging requests
            async with session.post(
                f"{self.api_base_url}/request", 
                json=request_data, 
                headers=headers,
                timeout=60  # 60 second timeout
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Error from Bright Data API: {error_text}")
                    return {"error": error_text, "status_code": response.status}
                
                try:
                    if data_format == "json":
                        return await response.json()
                    else:
                        content = await response.text()
                        return {"content": content, "status_code": response.status}
                except aiohttp.ContentTypeError as e:
                    # Handle case where response claims to be JSON but isn't
                    content = await response.text()
                    logger.error(f"Invalid content type received: {e}")
                    return {"error": f"Invalid content type: {str(e)}", "content": content}
                
        except aiohttp.ClientError as e:
            logger.error(f"Network error with Bright Data API: {e}")
            return {"error": f"Network error: {str(e)}"}
        except asyncio.TimeoutError:
            logger.error("Request to Bright Data API timed out")
            return {"error": "Request timed out"}
        except Exception as e:
            logger.error(f"Error making request to Bright Data API: {e}")
            return {"error": str(e)}
    
    async def search_engine(self, 
                           query: str, 
                           engine: str = "google", 
                           country_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Search using a search engine via Bright Data
        
        Args:
            query: Search query
            engine: Search engine to use (google, bing, yandex)
            country_code: Optional country code for geolocation
            
        Returns:
            Search results
        """
        query_encoded = quote_plus(query)
        url = self._get_search_engine_url(engine, query_encoded)
        
        return await self.request(
            url=url,
            browser_emulation=True,
            data_format="markdown",
            country_code=country_code
        )
    
    def _get_search_engine_url(self, engine: str, query: str) -> str:
        """Get the appropriate search engine URL based on the engine"""
        if engine == "bing":
            return f"https://www.bing.com/search?q={query}"
        elif engine == "yandex":
            return f"https://yandex.com/search/?text={query}"
        else:  # default to Google
            return f"https://www.google.com/search?q={query}"
    
    def _generate_mock_response(self, url: str) -> Dict[str, Any]:
        """Generate mock response data for testing when API key is not available"""
        logger.info(f"Generating mock response for URL: {url}")
        
        if "skyscanner.com" in url:
            return {
                "content": "<html><body>Mock Skyscanner flight data</body></html>",
                "status_code": 200
            }
        elif "booking.com" in url or "hotels.com" in url:
            return {
                "content": "<html><body>Mock hotel booking data</body></html>",
                "status_code": 200
            }
        elif "weather" in url or "forecast" in url:
            return {
                "content": "<html><body>Mock weather forecast data</body></html>",
                "status_code": 200
            }
        elif "events" in url or "tickets" in url:
            return {
                "content": "<html><body>Mock events and tickets data</body></html>",
                "status_code": 200
            }
        else:
            return {
                "content": f"<html><body>Mock data for {url}</body></html>",
                "status_code": 200
            }
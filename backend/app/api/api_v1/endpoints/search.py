from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import logging
import asyncio

from app import crud, schemas
from app.api import deps
from app.services.scraper.flight_scraper import FlightScraper
from app.services.scraper.hotel_scraper import HotelScraper
from app.services.scraper.weather_scraper import WeatherScraper
from app.services.scraper.event_scraper import EventScraper

logger = logging.getLogger(__name__)

router = APIRouter()


async def process_search_data(
    search_id: int,
    search_params: schemas.SearchCreate,
    flight_scraper: FlightScraper,
    hotel_scraper: HotelScraper,
    weather_scraper: WeatherScraper,
    event_scraper: EventScraper,
    db: Session,
) -> None:
    """
    Process search data asynchronously.
    This function runs as a background task to scrape flight, hotel, weather, and event data.
    """
    logger.info(f"Starting background processing for search_id: {search_id}")
    
    try:
        # Run scrapers in parallel
        flight_task = asyncio.create_task(flight_scraper.search_flights(
            origin=search_params.departure_location,
            destination=search_params.destination,
            departure_date=search_params.departure_date,
            return_date=search_params.return_date,
            adults=search_params.adults,
            children=search_params.children,
            cabin_class=search_params.preferences.get("cabin_class", "economy") if search_params.preferences else "economy"
        ))
        
        hotel_task = asyncio.create_task(hotel_scraper.search_hotels(
            destination=search_params.destination,
            check_in=search_params.departure_date,
            check_out=search_params.return_date,
            guests=search_params.adults + search_params.children,
            max_price=search_params.preferences.get("max_price") if search_params.preferences else None
        ))
        
        weather_task = asyncio.create_task(weather_scraper.get_weather_forecast(
            destination=search_params.destination,
            start_date=search_params.departure_date,
            end_date=search_params.return_date
        ))
        
        event_task = asyncio.create_task(event_scraper.get_events(
            destination=search_params.destination,
            start_date=search_params.departure_date,
            end_date=search_params.return_date
        ))
        
        # Wait for all tasks to complete
        flights_data, hotels_data, weather_data, events_data = await asyncio.gather(
            flight_task, hotel_task, weather_task, event_task
        )
        
        # Save flights to database
        for flight in flights_data:
            flight_data = schemas.FlightCreate(
                search_id=search_id,
                airline=flight.get("airline"),
                flight_number=flight.get("flight_number"),
                departure_airport=flight.get("departure_airport"),
                arrival_airport=flight.get("arrival_airport"),
                departure_time=flight.get("departure_time"),
                arrival_time=flight.get("arrival_time"),
                duration=flight.get("duration"),
                stops=flight.get("stops"),
                price=flight.get("price"),
                currency=flight.get("currency", "USD"),
                cabin_class=flight.get("cabin_class"),
                additional_info=flight.get("additional_info", {})
            )
            crud.flight.create(db=db, obj_in=flight_data)
        
        # Save hotels to database
        for hotel in hotels_data:
            hotel_data = schemas.HotelCreate(
                search_id=search_id,
                name=hotel.get("name"),
                address=hotel.get("address"),
                star_rating=hotel.get("star_rating"),
                price_per_night=hotel.get("price_per_night"),
                total_price=hotel.get("total_price"),
                currency=hotel.get("currency", "USD"),
                amenities=hotel.get("amenities", []),
                image_url=hotel.get("image_url"),
                booking_url=hotel.get("booking_url"),
                additional_info=hotel.get("additional_info", {})
            )
            crud.hotel.create(db=db, obj_in=hotel_data)
        
        # Save weather data to database
        for weather in weather_data:
            weather_obj = schemas.WeatherCreate(
                search_id=search_id,
                date=weather.get("date"),
                temperature_high=weather.get("temperature_high"),
                temperature_low=weather.get("temperature_low"),
                condition=weather.get("condition"),
                humidity=weather.get("humidity"),
                precipitation_chance=weather.get("precipitation_chance"),
                wind_speed=weather.get("wind_speed"),
                additional_info=weather.get("additional_info", {})
            )
            crud.weather.create(db=db, obj_in=weather_obj)
        
        # Save events to database
        for event in events_data:
            event_data = schemas.EventCreate(
                search_id=search_id,
                name=event.get("name"),
                date=event.get("date"),
                location=event.get("location"),
                description=event.get("description"),
                category=event.get("category"),
                price=event.get("price"),
                currency=event.get("currency", "USD"),
                booking_url=event.get("booking_url"),
                image_url=event.get("image_url"),
                additional_info=event.get("additional_info", {})
            )
            crud.event.create(db=db, obj_in=event_data)
        
        # Generate recommendations based on the collected data
        # This could be implemented in a separate AI service
        # For now, we'll just log that this would happen here
        logger.info(f"Would generate recommendations for search_id: {search_id}")
        
        # Update search record to mark as completed
        crud.search.update(db=db, db_obj=crud.search.get(db=db, id=search_id), 
                           obj_in={"status": "completed"})
        
        logger.info(f"Completed background processing for search_id: {search_id}")
    
    except Exception as e:
        logger.error(f"Error processing search_id {search_id}: {str(e)}")
        # Update search record to mark as failed
        crud.search.update(db=db, db_obj=crud.search.get(db=db, id=search_id), 
                           obj_in={"status": "failed", "error_message": str(e)})


@router.post("/scrape", response_model=schemas.SearchResponse)
async def scrape_travel_data(
    search_params: schemas.SearchCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
    flight_scraper: FlightScraper = Depends(deps.get_flight_scraper_dep),
    hotel_scraper: HotelScraper = Depends(deps.get_hotel_scraper_dep),
    weather_scraper: WeatherScraper = Depends(deps.get_weather_scraper_dep),
    event_scraper: EventScraper = Depends(deps.get_event_scraper_dep),
):
    """
    Trigger a scraping job for travel data based on search parameters using Bright Data.
    """
    # Create a new search in the database
    search = crud.search.create_with_owner(db=db, obj_in=search_params, owner_id=current_user.id)
    
    # Add the background task to scrape data
    background_tasks.add_task(
        process_search_data,
        search_id=search.id,
        search_params=search_params,
        flight_scraper=flight_scraper,
        hotel_scraper=hotel_scraper,
        weather_scraper=weather_scraper,
        event_scraper=event_scraper,
        db=db
    )
    
    return {
        "search_id": search.id,
        "status": "processing",
        "message": "Your search is being processed. Please check back soon for results."
    }


@router.get("/{search_id}", response_model=schemas.SearchResponse)
def get_search_results(
    search_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Get the results of a previous search.
    """
    search = crud.search.get(db=db, id=search_id)
    
    if not search:
        raise HTTPException(
            status_code=404,
            detail="Search not found"
        )
    
    # Check if the search belongs to the current user
    if search.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Get associated data
    flights = crud.flight.get_multi_by_search(db=db, search_id=search_id)
    hotels = crud.hotel.get_multi_by_search(db=db, search_id=search_id)
    weather_data = crud.weather.get_multi_by_search(db=db, search_id=search_id)
    events = crud.event.get_multi_by_search(db=db, search_id=search_id)
    recommendations = crud.recommendation.get_multi_by_search(db=db, search_id=search_id)
    
    return {
        "search": search,
        "flights": flights,
        "hotels": hotels,
        "weather_data": weather_data,
        "events": events,
        "recommendations": recommendations
    }


@router.delete("/{search_id}", response_model=schemas.Message)
def delete_search(
    search_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Delete a search and all its associated data.
    """
    search = crud.search.get(db=db, id=search_id)
    
    if not search:
        raise HTTPException(
            status_code=404,
            detail="Search not found"
        )
    
    # Check if the search belongs to the current user
    if search.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Delete the search and all associated data
    crud.search.remove(db=db, id=search_id)
    
    return {"message": "Search deleted successfully"}

"""
Test script for the PackingSuggestionGenerator with fallback mechanisms
"""
import sys
import os
import asyncio
import datetime, timedelta
from typing import Dict, Any, List

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.ai.packing_suggestion import PackingSuggestionGenerator

async def test_packing_suggestions():
    """Test packing suggestion generator including fallback mechanisms"""
    print("Testing PackingSuggestionGenerator...")
    
    # Sample weather data
    weather_data = [
        {
            "date": (datetime.datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
            "temperature_high": 75 + i,
            "temperature_low": 60 + i,
            "precipitation_chance": 20 if i % 2 == 0 else 10,
            "condition": "Sunny" if i % 3 == 0 else "Partly Cloudy"
        }
        for i in range(5)
    ]
    
    # Initialize generator without LLM client to test fallback behavior
    generator_no_llm = PackingSuggestionGenerator(llm_client=None)
    
    # Test with specific destination and dates
    destination = "Miami Beach"
    start_date = (datetime.datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = (datetime.datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    activities = ["swimming", "sightseeing", "dining", "nightlife"]
    
    try:
        # Test packing suggestion generation with fallback to rule-based approach
        print("\nGenerating packing suggestions using rule-based fallback...")
        suggestions = await generator_no_llm.generate_packing_suggestions(
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            weather_data=weather_data,
            activities=activities
        )
        
        # Print suggestions
        print(f"\nPacking suggestions for {destination}:")
        for category, items in suggestions.items():
            print(f"\n{category.capitalize()}:")
            for item in items:
                print(f"  - {item}")
                
        print("\nTest completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error testing packing suggestions: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_packing_suggestions())
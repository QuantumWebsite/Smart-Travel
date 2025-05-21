import logging
from typing import Dict, Any, List, Optional
import numpy as np
import datetime
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    AI recommendation engine that analyzes flights, hotels, weather, and events
    to make personalized travel recommendations
    """
    
    def __init__(self, llm_client=None):
        """
        Initialize with optional LLM client
        """
        self.llm_client = llm_client
    
    async def generate_recommendations(self, 
                                search_data: Dict[str, Any],
                                flights: List[Dict[str, Any]], 
                                hotels: List[Dict[str, Any]],
                                weather_data: List[Dict[str, Any]],
                                events: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Generate personalized travel recommendations
        
        Args:
            search_data: User search parameters
            flights: List of flight data
            hotels: List of hotel data
            weather_data: List of weather data
            events: List of event data (optional)
            
        Returns:
            List of recommendations with explanation and scores
        """
        if not flights or not hotels or not weather_data:
            return []
            
        # Calculate scores for each flight and hotel combination
        recommendations = self._generate_flight_hotel_combinations(flights, hotels, weather_data, events)
        
        # Add packing suggestions based on weather
        recommendations = self._add_packing_suggestions(recommendations, weather_data)
            
        # Sort recommendations by total score (descending)
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        
        # Keep only the top recommendations
        top_recommendations = recommendations[:5]
        
        # Generate textual summaries for the top recommendations
        top_recommendations = await self._generate_summaries(top_recommendations, search_data)
        
        return top_recommendations
        
    def _generate_flight_hotel_combinations(self, 
                                           flights: List[Dict[str, Any]], 
                                           hotels: List[Dict[str, Any]],
                                           weather_data: List[Dict[str, Any]],
                                           events: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Generate combinations of flights and hotels and score them
        """
        recommendations = []
        
        # Calculate average weather scores for the date range
        weather_scores = self._calculate_weather_scores(weather_data)
        
        # Generate combinations (limit to a reasonable number for demo purposes)
        max_combinations = 20
        counter = 0
        
        for flight in flights[:10]:  # Limit to top 10 flights for simplicity
            for hotel in hotels[:10]:  # Limit to top 10 hotels for simplicity
                if counter >= max_combinations:
                    break
                    
                # Calculate scores
                price_score = self._calculate_price_score(flight, hotel)
                convenience_score = self._calculate_convenience_score(flight, hotel)
                
                # Get weather score for this date range
                departure_date = datetime.fromisoformat(flight["departure_time"]) if isinstance(flight["departure_time"], str) else flight["departure_time"]
                arrival_time = datetime.fromisoformat(flight["arrival_time"]) if isinstance(flight["arrival_time"], str) else flight["arrival_time"]
                weather_score = self._get_weather_score_for_dates(weather_scores, departure_date.strftime("%Y-%m-%d"), arrival_time.strftime("%Y-%m-%d"))
                
                # Calculate total score (weighted average)
                total_score = (
                    0.4 * price_score +
                    0.4 * weather_score +
                    0.2 * convenience_score
                )
                
                recommendation = {
                    "flight": flight,
                    "hotel": hotel,
                    "score": total_score,
                    "price_score": price_score,
                    "weather_score": weather_score,
                    "convenience_score": convenience_score,
                    "total_price": flight["price"] + (hotel["price_per_night"] * self._calculate_nights(flight)),
                    "currency": flight["currency"]  # Assuming all prices are in the same currency
                }
                
                recommendations.append(recommendation)
                counter += 1
        
        return recommendations
    
    def _calculate_price_score(self, flight: Dict[str, Any], hotel: Dict[str, Any]) -> float:
        """
        Calculate price score based on flight and hotel prices
        Lower prices = higher score
        """
        # Simple scoring based on total price
        # In a real implementation, you would use more sophisticated pricing analysis
        flight_price = flight["price"]
        hotel_price_per_night = hotel["price_per_night"]
        nights = self._calculate_nights(flight)
        total_price = flight_price + (hotel_price_per_night * nights)
        
        # Inverse price score (lower price = higher score)
        # Scale between 0 and 1 (assuming prices between $100 and $2000)
        min_price = 100
        max_price = 2000
        
        # Clamp price within range
        clamped_price = max(min_price, min(total_price, max_price))
        
        # Calculate score (inverse: lower price = higher score)
        price_score = 1 - ((clamped_price - min_price) / (max_price - min_price))
        
        return price_score
    
    def _calculate_convenience_score(self, flight: Dict[str, Any], hotel: Dict[str, Any]) -> float:
        """
        Calculate convenience score based on flight duration, layovers, and hotel location
        """
        # Score based on flight duration (shorter = better)
        max_duration = 600  # in minutes
        duration_score = 1 - (min(flight["duration_minutes"], max_duration) / max_duration)
        
        # Score based on layovers (fewer = better)
        layovers_score = 1.0 if flight["layovers"] == 0 else (0.7 if flight["layovers"] == 1 else 0.4)
        
        # Hotel rating score
        rating_score = hotel.get("rating", 3.0) / 5.0
        
        # Combine scores (weighted average)
        convenience_score = (0.4 * duration_score + 0.3 * layovers_score + 0.3 * rating_score)
        
        return convenience_score
    
    def _calculate_weather_scores(self, weather_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate weather scores for each date
        """
        weather_scores = {}
        
        for day_weather in weather_data:
            date_str = day_weather["date"] if isinstance(day_weather["date"], str) else day_weather["date"].strftime("%Y-%m-%d")
            
            # Good weather score based on:
            # - Temperature (ideal range: 70-85°F)
            # - Low precipitation chance
            # - Good conditions (Sunny, Clear, Partly Cloudy)
            
            # Temperature score
            temp_high = day_weather["temperature_high"]
            ideal_temp_low = 70
            ideal_temp_high = 85
            
            if ideal_temp_low <= temp_high <= ideal_temp_high:
                temp_score = 1.0
            else:
                # How far from ideal range
                if temp_high < ideal_temp_low:
                    temp_diff = ideal_temp_low - temp_high
                else:
                    temp_diff = temp_high - ideal_temp_high
                    
                # Max penalty of 0.5 for being 20 degrees away from ideal range
                temp_score = max(0.5, 1.0 - (temp_diff / 40.0))
            
            # Precipitation score (0% = 1.0, 100% = 0.0)
            precip_score = 1.0 - (day_weather["precipitation_chance"] / 100.0)
            
            # Condition score
            condition = day_weather["condition"]
            good_conditions = ["Sunny", "Clear", "Partly Cloudy"]
            neutral_conditions = ["Cloudy"]
            
            if condition in good_conditions:
                condition_score = 1.0
            elif condition in neutral_conditions:
                condition_score = 0.7
            else:
                condition_score = 0.3
            
            # Final weather score (weighted)
            weather_score = (0.4 * temp_score + 0.4 * precip_score + 0.2 * condition_score)
            weather_scores[date_str] = weather_score
        
        return weather_scores
    
    def _get_weather_score_for_dates(self, weather_scores: Dict[str, float],
                                    start_date: str, end_date: str) -> float:
        """
        Get the average weather score for a date range
        """
        # Convert strings to datetime objects for easier comparison
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        relevant_scores = []
        
        for date_str, score in weather_scores.items():
            date = datetime.strptime(date_str, "%Y-%m-%d")
            if start <= date <= end:
                relevant_scores.append(score)
        
        if not relevant_scores:
            return 0.5  # Default score if no weather data available
            
        return sum(relevant_scores) / len(relevant_scores)
    
    def _calculate_nights(self, flight: Dict[str, Any]) -> int:
        """
        Calculate the number of nights between departure and arrival dates
        """
        departure_date = datetime.fromisoformat(flight["departure_time"]) if isinstance(flight["departure_time"], str) else flight["departure_time"]
        arrival_time = datetime.fromisoformat(flight["arrival_time"]) if isinstance(flight["arrival_time"], str) else flight["arrival_time"]
        
        # Calculate nights (assuming departure and return flights)
        nights = (arrival_time - departure_date).days
        
        # Ensure at least 1 night
        return max(1, nights)
    
    def _add_packing_suggestions(self, recommendations: List[Dict[str, Any]], 
                               weather_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Add packing suggestions based on weather forecast
        """
        for recommendation in recommendations:
            flight = recommendation["flight"]
            
            # Get date range for this recommendation
            departure_date = datetime.fromisoformat(flight["departure_time"]) if isinstance(flight["departure_time"], str) else flight["departure_time"]
            arrival_time = datetime.fromisoformat(flight["arrival_time"]) if isinstance(flight["arrival_time"], str) else flight["arrival_time"]
            
            # Find min/max temperatures and predominant conditions
            temps = []
            conditions = []
            
            for day_weather in weather_data:
                date = datetime.strptime(day_weather["date"], "%Y-%m-%d") if isinstance(day_weather["date"], str) else day_weather["date"]
                
                if departure_date.date() <= date.date() <= arrival_time.date():
                    temps.append(day_weather["temperature_high"])
                    temps.append(day_weather["temperature_low"])
                    conditions.append(day_weather["condition"])
            
            if not temps:
                # No weather data for this period
                recommendation["packing_suggestions"] = {
                    "clothing": ["Pack for variable weather, layering recommended"],
                    "accessories": ["Sunglasses", "Umbrella (just in case)"],
                    "documents": ["Passport", "ID", "Hotel confirmation", "Travel insurance"]
                }
                continue
                
            min_temp = min(temps)
            max_temp = max(temps)
            
            # Determine predominant conditions
            from collections import Counter
            condition_counts = Counter(conditions)
            predominant_condition = condition_counts.most_common(1)[0][0]
            
            # Generate packing suggestions based on temperature and conditions
            clothing = ["Comfortable walking shoes"]
            accessories = ["Smartphone charger", "Travel adapter"]
            documents = ["Passport", "ID", "Hotel confirmation", "Travel insurance"]
            
            # Temperature-based clothing
            if min_temp < 50:
                clothing.extend(["Winter coat", "Sweaters", "Long pants", "Warm socks"])
            elif min_temp < 65:
                clothing.extend(["Light jacket", "Long-sleeve shirts", "Pants"])
            else:
                clothing.extend(["T-shirts", "Shorts/skirts"])
                
            if max_temp > 80:
                clothing.extend(["Light, breathable clothing"])
                accessories.append("Hat")
                
            # Condition-based items
            if "Rain" in predominant_condition or "Thunderstorm" in predominant_condition:
                accessories.extend(["Umbrella", "Raincoat"])
            
            if "Sunny" in predominant_condition or "Clear" in predominant_condition:
                accessories.extend(["Sunglasses", "Sunscreen"])
            
            recommendation["packing_suggestions"] = {
                "clothing": clothing,
                "accessories": accessories,
                "documents": documents
            }
            
        return recommendations
    
    async def _generate_summaries(self, recommendations: List[Dict[str, Any]], 
                                search_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate text summaries for recommendations using LLM
        """
        for recommendation in recommendations:
            flight = recommendation["flight"]
            hotel = recommendation["hotel"]
            
            # For demonstration, generate a simple summary
            # In a real implementation, you would use the LLM client to generate these
            
            # Price comparison
            avg_price = 1000  # Placeholder for average price
            price_diff_percent = ((avg_price - recommendation["total_price"]) / avg_price) * 100
            
            price_text = f"{abs(price_diff_percent):.0f}% cheaper than average" if price_diff_percent > 0 else \
                        f"{abs(price_diff_percent):.0f}% more expensive than average"
                        
            # Weather text
            weather_score = recommendation["weather_score"]
            if weather_score > 0.8:
                weather_text = "excellent weather conditions"
            elif weather_score > 0.6:
                weather_text = "good weather conditions"
            else:
                weather_text = "acceptable weather conditions"
                
            # Convenience text
            convenience_score = recommendation["convenience_score"]
            if convenience_score > 0.8:
                convenience_text = f"convenient {flight['duration_minutes'] // 60}h{flight['duration_minutes'] % 60}m non-stop flight"
            elif convenience_score > 0.6:
                convenience_text = f"reasonable {flight['duration_minutes'] // 60}h{flight['duration_minutes'] % 60}m flight"
            else:
                convenience_text = f"{flight['duration_minutes'] // 60}h{flight['duration_minutes'] % 60}m flight with {flight['layovers']} layover(s)"
            
            # Generate summary
            summary = (
                f"This {price_text} deal features a {convenience_text} with {flight['airline']} "
                f"and a stay at the {hotel['rating']}-star {hotel['name']} in {hotel['location']}. "
                f"You can expect {weather_text} during your trip."
            )
            
            # Add LLM-generated summary if available
            if self.llm_client:
                llm_summary = await self._get_llm_summary(recommendation, search_data)
                if llm_summary:
                    summary = llm_summary
            
            recommendation["summary"] = summary
            
        return recommendations
        
    async def _get_llm_summary(self, recommendation: Dict[str, Any], 
                             search_data: Dict[str, Any]) -> str:
        """
        Get LLM-generated summary for a recommendation
        """
        try:
            if not self.llm_client:
                return None
                
            # Build prompt for LLM
            prompt_template = self._build_llm_prompt(recommendation, search_data)
            
            # Create LangChain PromptTemplate
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=[]  # No input variables as we've already filled the template
            )
            
            # Create LangChain chain
            chain = LLMChain(llm=self.llm_client, prompt=prompt)
            
            # Generate summary
            summary = await chain.arun({})
            
            return summary
        except Exception as e:
            logger.error(f"Error generating LLM summary: {e}")
            return None
            
    def _build_llm_prompt(self, recommendation: Dict[str, Any], 
                        search_data: Dict[str, Any]) -> str:
        """
        Build prompt for LLM to generate recommendation summary
        """
        flight = recommendation["flight"]
        hotel = recommendation["hotel"]
        
        prompt = f"""
        Generate a concise, engaging travel recommendation summary based on the following details:
        
        User search:
        - Origin: {search_data.get('origin', 'Unknown')}
        - Destination: {search_data.get('destination', 'Unknown')}
        - Travel dates: {flight['departure_time']} to {flight['arrival_time']}
        - Number of travelers: {search_data.get('travelers', 1)}
        
        Flight details:
        - Airline: {flight['airline']}
        - Duration: {flight['duration_minutes'] // 60}h{flight['duration_minutes'] % 60}m
        - Layovers: {flight['layovers']}
        - Price: ${flight['price']}
        
        Hotel details:
        - Name: {hotel['name']}
        - Location: {hotel['location']}
        - Rating: {hotel['rating']}/5
        - Price: ${hotel['price_per_night']} per night
        
        Scores:
        - Overall score: {recommendation['score']:.2f}/1.00
        - Price score: {recommendation['price_score']:.2f}/1.00
        - Weather score: {recommendation['weather_score']:.2f}/1.00
        - Convenience score: {recommendation['convenience_score']:.2f}/1.00
        
        Include:
        1. Whether this is a good deal compared to average prices
        2. Weather expectations during the stay
        3. Highlights about the flight and hotel
        4. Why this is recommended (value, convenience, etc.)
        
        Keep the summary to 2-3 sentences maximum.
        """
        
        return prompt

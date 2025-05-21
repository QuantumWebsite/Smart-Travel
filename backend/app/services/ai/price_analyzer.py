import logging
from typing import Dict, Any, List, Optional
import datetime, timedelta
import numpy as np

logger = logging.getLogger(__name__)


class PriceAnalyzer:
    """
    Analyzes flight and hotel price data to identify trends, good deals,
    and optimal booking times.
    """
    
    def __init__(self):
        """Initialize the price analyzer"""
        pass
    
    def find_best_deals(self, 
                      flights: List[Dict[str, Any]], 
                      hotels: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Find the best deals among flights and hotels
        
        Args:
            flights: List of flight data
            hotels: List of hotel data
            
        Returns:
            List of best deals with explanations
        """
        best_deals = []
        
        if flights:
            best_flight_deals = self._find_best_flight_deals(flights)
            best_deals.extend(best_flight_deals)
            
        if hotels:
            best_hotel_deals = self._find_best_hotel_deals(hotels)
            best_deals.extend(best_hotel_deals)
            
        return best_deals
    
    def _find_best_flight_deals(self, flights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find the best flight deals"""
        if not flights:
            return []
            
        # Calculate average price
        prices = [flight["price"] for flight in flights]
        avg_price = sum(prices) / len(prices)
        
        best_deals = []
        for flight in flights:
            price_diff = avg_price - flight["price"]
            savings_percent = (price_diff / avg_price) * 100
            
            # Only consider as a deal if it's at least 15% cheaper
            if savings_percent >= 15:
                deal = {
                    "type": "flight",
                    "item": flight,
                    "savings_percent": savings_percent,
                    "savings_amount": price_diff,
                    "avg_price": avg_price,
                    "explanation": f"{flight['airline']} flight is {savings_percent:.1f}% cheaper than average for this route."
                }
                best_deals.append(deal)
        
        # Sort by savings percentage
        best_deals.sort(key=lambda x: x["savings_percent"], reverse=True)
        
        # Limit to top 3
        return best_deals[:3]
    
    def _find_best_hotel_deals(self, hotels: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find the best hotel deals"""
        if not hotels:
            return []
            
        # Calculate average price per night for different star ratings
        star_prices = {}
        for hotel in hotels:
            rating = round(hotel["rating"]) if "rating" in hotel else 3
            if rating not in star_prices:
                star_prices[rating] = []
            star_prices[rating].append(hotel["price_per_night"])
        
        # Calculate average price per star rating
        avg_prices = {
            rating: sum(prices) / len(prices) 
            for rating, prices in star_prices.items() if prices
        }
        
        best_deals = []
        for hotel in hotels:
            rating = round(hotel["rating"]) if "rating" in hotel else 3
            
            if rating in avg_prices:
                avg_price = avg_prices[rating]
                price_diff = avg_price - hotel["price_per_night"]
                savings_percent = (price_diff / avg_price) * 100
                
                # Only consider as a deal if it's at least 15% cheaper for same star rating
                if savings_percent >= 15:
                    deal = {
                        "type": "hotel",
                        "item": hotel,
                        "savings_percent": savings_percent,
                        "savings_amount": price_diff,
                        "avg_price": avg_price,
                        "explanation": f"{hotel['name']} is {savings_percent:.1f}% cheaper than average for {rating}-star hotels in this area."
                    }
                    best_deals.append(deal)
        
        # Sort by savings percentage
        best_deals.sort(key=lambda x: x["savings_percent"], reverse=True)
        
        # Limit to top 3
        return best_deals[:3]
    
    def analyze_price_trends(self, 
                          historical_prices: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze historical price trends
        
        Args:
            historical_prices: List of historical price data points
                Each item should have 'date' and 'price' keys
                
        Returns:
            Dictionary with trend analysis
        """
        if not historical_prices or len(historical_prices) < 3:
            return {
                "trend": "unknown",
                "direction": "stable",
                "confidence": 0,
                "recommendation": "Not enough data to analyze price trends."
            }
        
        # Sort by date
        sorted_prices = sorted(historical_prices, key=lambda x: x["date"])
        
        # Extract dates and prices
        dates = [item["date"] for item in sorted_prices]
        prices = [item["price"] for item in sorted_prices]
        
        # Calculate simple trend (linear regression would be better with more data)
        first_third = np.mean(prices[:len(prices)//3])
        last_third = np.mean(prices[-len(prices)//3:])
        price_diff = last_third - first_third
        
        # Determine trend direction
        if price_diff > 0.05 * first_third:
            direction = "increasing"
            recommendation = "Consider booking soon as prices are trending upward."
        elif price_diff < -0.05 * first_third:
            direction = "decreasing"
            recommendation = "Consider waiting as prices are trending downward."
        else:
            direction = "stable"
            recommendation = "Prices are relatively stable, book at your convenience."
        
        # Calculate confidence based on consistency of trend
        price_changes = [prices[i+1] - prices[i] for i in range(len(prices) - 1)]
        consistent_direction = all(pc > 0 for pc in price_changes) or all(pc < 0 for pc in price_changes)
        
        if consistent_direction:
            confidence = 0.8
        else:
            # Calculate how many price changes are in the dominant direction
            increasing_changes = sum(1 for pc in price_changes if pc > 0)
            decreasing_changes = sum(1 for pc in price_changes if pc < 0)
            dominant_direction_count = max(increasing_changes, decreasing_changes)
            confidence = dominant_direction_count / len(price_changes)
        
        return {
            "trend": "historical",
            "direction": direction,
            "confidence": confidence,
            "recommendation": recommendation,
            "price_diff_percent": (price_diff / first_third) * 100 if first_third else 0
        }
    
    def predict_optimal_booking_time(self, 
                                  destination: str, 
                                  travel_dates: Dict[str, str],
                                  historical_data: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Predict the optimal time to book flights and hotels
        
        Args:
            destination: Destination location
            travel_dates: Dictionary with start_date and end_date
            historical_data: Optional historical pricing data
            
        Returns:
            Dictionary with booking recommendations
        """
        # In a real implementation, this would use historical data and ML models
        # For now, returning simplified recommendations based on general travel trends
        
        departure_date = datetime.strptime(travel_dates["start_date"], "%Y-%m-%d")
        days_until_departure = (departure_date - datetime.datetime.now()).days
        
        flight_recommendation = {}
        hotel_recommendation = {}
        
        # Flight booking recommendations
        if days_until_departure > 90:
            flight_recommendation = {
                "recommendation": "Monitor prices but wait",
                "explanation": "For most destinations, the best flight deals typically appear 2-3 months before departure. Continue monitoring prices."
            }
        elif 30 < days_until_departure <= 90:
            flight_recommendation = {
                "recommendation": "Good time to book flights",
                "explanation": "This is generally the optimal window to book flights. Prices tend to be lower 1-3 months before departure."
            }
        elif 14 < days_until_departure <= 30:
            flight_recommendation = {
                "recommendation": "Book flights soon",
                "explanation": "Flight prices typically increase as the departure date approaches. Consider booking soon to avoid higher fares."
            }
        else:
            flight_recommendation = {
                "recommendation": "Book flights immediately",
                "explanation": "Flight prices usually increase significantly within 2 weeks of departure. Book as soon as possible."
            }
            
        # Hotel booking recommendations
        if days_until_departure > 60:
            hotel_recommendation = {
                "recommendation": "Wait to book hotels",
                "explanation": "For most destinations, it's too early to book hotels. Better rates typically appear closer to your stay."
            }
        elif 30 < days_until_departure <= 60:
            hotel_recommendation = {
                "recommendation": "Consider booking refundable rates",
                "explanation": "You can book refundable hotel rates now and continue monitoring for better deals."
            }
        elif 7 < days_until_departure <= 30:
            hotel_recommendation = {
                "recommendation": "Good time to book hotels",
                "explanation": "This is generally a good time to book hotels. Availability is still good and prices are reasonable."
            }
        else:
            hotel_recommendation = {
                "recommendation": "Book hotels immediately",
                "explanation": "With less than a week before your trip, hotel availability may be limited. Book as soon as possible."
            }
            
        # Add destination-specific adjustments
        if "beach" in destination.lower() or "island" in destination.lower():
            if 3 <= departure_date.month <= 8:  # Summer months
                flight_recommendation["explanation"] += " Beach destinations are popular during summer, so prices may be higher."
                hotel_recommendation["explanation"] += " Beach destinations fill up quickly during summer months."
                
        elif "ski" in destination.lower() or "mountain" in destination.lower():
            if departure_date.month in [1, 2, 12]:  # Winter peak season
                flight_recommendation["explanation"] += " Ski destinations are in high demand during winter peak season."
                hotel_recommendation["explanation"] += " Ski resorts often fill up quickly during peak season."
        
        return {
            "flights": flight_recommendation,
            "hotels": hotel_recommendation,
            "days_until_departure": days_until_departure
        }

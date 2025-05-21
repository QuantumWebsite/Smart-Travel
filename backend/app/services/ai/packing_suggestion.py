import logging
from typing import Dict, Any, List, Optional
try:
    # Try importing from new location (langchain_community)
    from langchain_community.llms import GoogleGenerativeAI
except ImportError:
    try:
        # Fallback to old location (deprecated)
        from langchain.llms import GoogleGenerativeAI
    except ImportError:
        # Define a placeholder to avoid import errors
        GoogleGenerativeAI = None
        logging.warning("GoogleGenerativeAI could not be imported. LLM features will be disabled.")
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

logger = logging.getLogger(__name__)


class PackingSuggestionGenerator:
    """
    Generates personalized packing suggestions based on weather data,
    destination, and trip details
    """
    def __init__(self, llm_client=None):
        """
        Initialize with Gemini or another LLM client
        """
        self.llm_client = llm_client
        if not self.llm_client and GoogleGenerativeAI is not None:
            try:
                # Initialize Gemini client using settings from environment
                from app.core.config import settings
                
                self.llm_client = GoogleGenerativeAI(
                    model=settings.GEMINI_MODEL,
                    google_api_key=settings.GEMINI_API_KEY,
                    temperature=0.7
                )
                logger.info(f"Initialized Gemini client with model: {settings.GEMINI_MODEL}")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}")
        elif not self.llm_client:
            logger.warning("GoogleGenerativeAI is not available, LLM functionality will be disabled")
    
    async def generate_packing_suggestions(self, 
                                        destination: str,
                                        start_date: str,
                                        end_date: str,
                                        weather_data: List[Dict[str, Any]],
                                        activities: Optional[List[str]] = None) -> Dict[str, List[str]]:
        """
        Generate packing suggestions based on weather and trip details
        
        Args:
            destination: Destination location
            start_date: Trip start date
            end_date: Trip end date
            weather_data: List of weather data for each day
            activities: Optional list of planned activities
            
        Returns:
            Dictionary with packing categories and item lists
        """
        try:
            # Extract key weather insights
            weather_insights = self._analyze_weather(weather_data)
            
            if self.llm_client:
                # Use LLM to generate personalized suggestions
                return await self._generate_llm_suggestions(destination, start_date, end_date, 
                                                         weather_insights, activities)
            else:
                # Fallback to rule-based suggestions
                return self._generate_rule_based_suggestions(weather_insights, activities)
        except Exception as e:
            logger.error(f"Error generating packing suggestions: {e}")
            # Return basic suggestions as fallback
            return self._generate_basic_suggestions()
    
    def _analyze_weather(self, weather_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze weather data to extract key insights for packing
        """
        if not weather_data:
            return {
                "min_temp": 60,
                "max_temp": 75,
                "avg_temp": 68,
                "precipitation_days": 0,
                "predominant_condition": "Unknown"
            }
            
        # Extract temperatures
        temps = []
        precipitation_days = 0
        conditions = []
        
        for day in weather_data:
            temps.append(day["temperature_high"])
            temps.append(day["temperature_low"])
            
            if day["precipitation_chance"] > 30:
                precipitation_days += 1
                
            conditions.append(day["condition"])
        
        # Find predominant condition
        from collections import Counter
        condition_counter = Counter(conditions)
        predominant_condition = condition_counter.most_common(1)[0][0]
        
        return {
            "min_temp": min(temps),
            "max_temp": max(temps),
            "avg_temp": sum(temps) / len(temps),
            "precipitation_days": precipitation_days,
            "predominant_condition": predominant_condition
        }
    
    async def _generate_llm_suggestions(self, 
                                     destination: str,
                                     start_date: str,
                                     end_date: str,
                                     weather_insights: Dict[str, Any],
                                     activities: Optional[List[str]] = None) -> Dict[str, List[str]]:
        """
        Generate packing suggestions using LLM
        """
        activities_str = ", ".join(activities) if activities else "sightseeing, dining, and relaxation"
        
        # Create prompt
        prompt_template = """
        Generate a comprehensive packing list for a trip to {destination} from {start_date} to {end_date}.
        
        Weather conditions during the trip:
        - Lowest temperature: {min_temp}°F
        - Highest temperature: {max_temp}°F
        - Average temperature: {avg_temp:.1f}°F
        - Days with precipitation: {precipitation_days}
        - Predominant condition: {predominant_condition}
        
        Planned activities: {activities}
        
        Provide packing suggestions organized into these categories:
        1. Clothing
        2. Accessories
        3. Toiletries
        4. Documents
        5. Electronics
        6. Miscellaneous
        
        Format each category as a bullet list. Be specific and practical.
        """
        
        # Create LangChain prompt
        prompt = PromptTemplate(
            input_variables=["destination", "start_date", "end_date", "min_temp", 
                            "max_temp", "avg_temp", "precipitation_days", 
                            "predominant_condition", "activities"],
            template=prompt_template
        )
        
        # Create LangChain chain
        chain = LLMChain(llm=self.llm_client, prompt=prompt)
        
        # Generate result
        result = await chain.arun(
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            min_temp=weather_insights["min_temp"],
            max_temp=weather_insights["max_temp"],
            avg_temp=weather_insights["avg_temp"],
            precipitation_days=weather_insights["precipitation_days"],
            predominant_condition=weather_insights["predominant_condition"],
            activities=activities_str
        )
        
        # Parse result into categories
        return self._parse_llm_output(result)
    
    def _parse_llm_output(self, llm_output: str) -> Dict[str, List[str]]:
        """
        Parse LLM output into structured categories
        """
        categories = {
            "clothing": [],
            "accessories": [],
            "toiletries": [],
            "documents": [],
            "electronics": [],
            "miscellaneous": []
        }
        
        # Simple parsing logic - could be improved with regex
        current_category = None
        
        for line in llm_output.split("\n"):
            line = line.strip()
            
            if not line:
                continue
                
            # Check for category headers
            lower_line = line.lower()
            if "clothing" in lower_line and ":" in line:
                current_category = "clothing"
                continue
            elif "accessories" in lower_line and ":" in line:
                current_category = "accessories"
                continue
            elif "toiletries" in lower_line and ":" in line:
                current_category = "toiletries"
                continue
            elif "documents" in lower_line and ":" in line:
                current_category = "documents"
                continue
            elif "electronics" in lower_line and ":" in line:
                current_category = "electronics"
                continue
            elif "miscellaneous" in lower_line and ":" in line or "misc" in lower_line and ":" in line:
                current_category = "miscellaneous"
                continue
                
            # Add items to current category
            if current_category and (line.startswith("-") or line.startswith("•")):
                item = line[1:].strip()
                categories[current_category].append(item)
        
        return categories
    
    def _generate_rule_based_suggestions(self, 
                                        weather_insights: Dict[str, Any],
                                        activities: Optional[List[str]] = None) -> Dict[str, List[str]]:
        """
        Generate packing suggestions using rule-based approach
        """
        suggestions = {
            "clothing": [],
            "accessories": [],
            "toiletries": ["Toothbrush", "Toothpaste", "Shampoo", "Conditioner", "Body wash", "Deodorant"],
            "documents": ["Passport", "Travel insurance", "Boarding passes", "Hotel reservations"],
            "electronics": ["Phone", "Charger", "Power bank"],
            "miscellaneous": ["Medications", "Hand sanitizer"]
        }
        
        # Add clothing based on temperature
        min_temp = weather_insights["min_temp"]
        max_temp = weather_insights["max_temp"]
        precipitation_days = weather_insights["precipitation_days"]
        
        # Basic clothing
        suggestions["clothing"].extend(["Underwear", "Socks", "Pajamas"])
        
        # Temperature-specific clothing
        if min_temp < 50:
            suggestions["clothing"].extend(["Winter coat", "Sweaters", "Long-sleeve shirts", "Warm socks", "Jeans/pants"])
            suggestions["accessories"].extend(["Gloves", "Scarf", "Winter hat"])
        elif min_temp < 65:
            suggestions["clothing"].extend(["Light jacket", "Long-sleeve shirts", "Sweatshirts", "Jeans/pants"])
            suggestions["accessories"].append("Light scarf")
        else:
            suggestions["clothing"].extend(["T-shirts", "Light shirts"])
            
        if max_temp > 75:
            suggestions["clothing"].extend(["Shorts", "T-shirts", "Light clothing"])
            suggestions["accessories"].extend(["Sunglasses", "Hat"])
            suggestions["toiletries"].append("Sunscreen")
        
        # Rain gear if needed
        if precipitation_days > 0:
            suggestions["accessories"].extend(["Umbrella", "Rain jacket"])
            if precipitation_days > 3:
                suggestions["clothing"].append("Waterproof shoes")
        
        # Activity-specific items
        if activities:
            if "beach" in " ".join(activities).lower() or "swimming" in " ".join(activities).lower():
                suggestions["clothing"].extend(["Swimsuit", "Beach cover-up"])
                suggestions["accessories"].extend(["Beach towel", "Flip flops"])
            
            if "hiking" in " ".join(activities).lower() or "trekking" in " ".join(activities).lower():
                suggestions["clothing"].extend(["Hiking pants", "Moisture-wicking shirts"])
                suggestions["accessories"].extend(["Hiking boots", "Backpack", "Water bottle"])
            
            if "business" in " ".join(activities).lower() or "meeting" in " ".join(activities).lower():
                suggestions["clothing"].extend(["Business attire", "Formal shoes"])
                suggestions["accessories"].append("Portfolio/briefcase")
        
        return suggestions
    
    def _generate_basic_suggestions(self) -> Dict[str, List[str]]:
        """
        Generate basic packing suggestions as fallback
        """
        return {
            "clothing": ["T-shirts", "Pants/jeans", "Underwear", "Socks", "Pajamas", "Light jacket"],
            "accessories": ["Sunglasses", "Hat", "Umbrella"],
            "toiletries": ["Toothbrush", "Toothpaste", "Shampoo", "Deodorant", "Sunscreen"],
            "documents": ["Passport", "ID", "Credit cards", "Insurance information"],
            "electronics": ["Phone", "Charger", "Camera", "Adapters"],
            "miscellaneous": ["Medications", "Books/e-reader", "Travel pillow"]
        }

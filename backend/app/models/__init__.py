# Import all models here
from .event import Event
from .search import Search
from .flight import Flight
from .hotel import Hotel
from .notification import Notification
from .packing_suggestion import PackingSuggestion
from .recommendation import Recommendation
from .saved_deal import SavedDeal
from .user import User
from .weather import Weather

__all_models = [
    Event,
    Search,
    Flight,
    Hotel,
    Notification,
    PackingSuggestion,
    Recommendation,
    SavedDeal,
    User,
    Weather,
]
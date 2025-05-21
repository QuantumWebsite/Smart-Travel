# Import all schemas here
from app.schemas.base_schema import Message, ErrorResponse, ResponseList
from app.schemas.search import Search, SearchCreate, SearchUpdate, SearchWithResults, SearchResponse
from app.schemas.user import User, UserCreate, UserUpdate, UserInDB
from app.schemas.token import Token, TokenPayload
from app.schemas.recommendation import Recommendation, RecommendationCreate, RecommendationUpdate
from app.schemas.packing_suggestion import PackingSuggestion, PackingSuggestionCreate, PackingSuggestionUpdate
from app.schemas.deal import SavedDeal, SavedDealCreate, SavedDealUpdate
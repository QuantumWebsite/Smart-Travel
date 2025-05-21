from typing import List

from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.recommendation import Recommendation
from app.models.search import Search
from app.schemas.recommendation import RecommendationCreate, RecommendationUpdate


class CRUDRecommendation(CRUDBase[Recommendation, RecommendationCreate, RecommendationUpdate]):
    """
    CRUD operations for Recommendation
    """
    
    def get_multi_by_user(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> List[Recommendation]:
        """
        Get recommendations for a specific user by joining with the search table
        
        Args:
            db: Database session
            user_id: ID of the user
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of recommendations for the user
        """
        return (
            db.query(Recommendation)
            .join(Search, Recommendation.search_id == Search.id)
            .filter(Search.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


recommendation = CRUDRecommendation(Recommendation)

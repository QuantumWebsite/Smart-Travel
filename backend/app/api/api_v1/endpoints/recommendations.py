from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Recommendation])
def get_recommendations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Get all recommendations for the current user.
    """
    print('Recommendations endpoint called')
    recommendations = crud.recommendation.get_multi_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    
    print(f"Recommendations found: {len(recommendations)}")
    return recommendations


@router.get("/{recommendation_id}", response_model=schemas.Recommendation)
def get_recommendation(
    recommendation_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Get a specific recommendation by ID.
    """
    recommendation = crud.recommendation.get(db=db, id=recommendation_id)
    
    if not recommendation:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found"
        )
    
    # Check if the recommendation's search belongs to the current user
    search = crud.search.get(db=db, id=recommendation.search_id)
    
    if not search or search.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return recommendation


@router.get("/{recommendation_id}/packing-suggestions", response_model=List[schemas.PackingSuggestion])
def get_packing_suggestions(
    recommendation_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Get packing suggestions for a specific recommendation.
    """
    recommendation = crud.recommendation.get(db=db, id=recommendation_id)
    
    if not recommendation:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found"
        )
    
    # Check if the recommendation's search belongs to the current user
    search = crud.search.get(db=db, id=recommendation.search_id)
    
    if not search or search.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    packing_suggestions = crud.packing_suggestion.get_multi_by_recommendation(
        db=db, recommendation_id=recommendation_id
    )
    
    return packing_suggestions

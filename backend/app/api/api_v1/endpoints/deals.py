from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.SavedDeal])
def get_all_deals(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Get all saved deals for the current user.
    """
    deals = crud.saved_deal.get_multi_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return deals


@router.post("/", response_model=schemas.SavedDeal)
def create_deal(
    deal_in: schemas.SavedDealCreate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Save a new deal.
    """
    # Check if recommendation exists and belongs to the user
    recommendation = crud.recommendation.get(db=db, id=deal_in.recommendation_id)
    
    if not recommendation:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found"
        )
    
    search = crud.search.get(db=db, id=recommendation.search_id)
    
    if not search or search.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Create saved deal
    deal = crud.saved_deal.create_with_owner(
        db=db, obj_in=deal_in, owner_id=current_user.id
    )
    
    return deal


@router.get("/{deal_id}", response_model=schemas.SavedDeal)
def get_deal(
    deal_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Get a specific saved deal by ID.
    """
    deal = crud.saved_deal.get(db=db, id=deal_id)
    
    if not deal:
        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )
    
    if deal.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return deal


@router.delete("/{deal_id}", response_model=schemas.Message)
def delete_deal(
    deal_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Delete a saved deal.
    """
    deal = crud.saved_deal.get(db=db, id=deal_id)
    
    if not deal:
        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )
    
    if deal.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    crud.saved_deal.remove(db=db, id=deal_id)
    
    return {"message": "Deal deleted successfully"}

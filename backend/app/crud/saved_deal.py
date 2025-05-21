from app.crud.base import CRUDBase
from app.models.saved_deal import SavedDeal
from app.schemas.deal import SavedDealCreate, SavedDealUpdate


class CRUDSavedDeal(CRUDBase[SavedDeal, SavedDealCreate, SavedDealUpdate]):
    """
    CRUD operations for SavedDeal
    """
    pass


saved_deal = CRUDSavedDeal(SavedDeal)

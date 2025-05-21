from app.crud.base import CRUDBase
from app.models.packing_suggestion import PackingSuggestion
from app.schemas.packing_suggestion import PackingSuggestionCreate, PackingSuggestionUpdate


class CRUDPackingSuggestion(CRUDBase[PackingSuggestion, PackingSuggestionCreate, PackingSuggestionUpdate]):
    """
    CRUD operations for PackingSuggestion
    """
    pass


packing_suggestion = CRUDPackingSuggestion(PackingSuggestion)

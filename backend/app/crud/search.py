from app.crud.base import CRUDBase
from app.models.search import Search
from app.schemas.search import SearchCreate, SearchUpdate


class CRUDSearch(CRUDBase[Search, SearchCreate, SearchUpdate]):
    """
    CRUD operations for Search
    """
    pass


search = CRUDSearch(Search)

from app.crud.base import CRUDBase
from app.models.event import Event
from app.schemas.base_schema import DefaultCreate, DefaultUpdate


class CRUDEvent(CRUDBase[Event, DefaultCreate, DefaultUpdate]):
    """
    CRUD operations for Event
    """
    pass


event = CRUDEvent(Event)

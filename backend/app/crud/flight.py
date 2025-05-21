from app.crud.base import CRUDBase
from app.models.flight import Flight
from app.schemas.base_schema import DefaultCreate, DefaultUpdate


class CRUDFlight(CRUDBase[Flight, DefaultCreate, DefaultUpdate]):
    pass


flight = CRUDFlight(Flight)

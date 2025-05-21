from app.crud.base import CRUDBase
from app.models.hotel import Hotel
from app.schemas.base_schema import DefaultCreate, DefaultUpdate


class CRUDHotel(CRUDBase[Hotel, DefaultCreate, DefaultUpdate]):
    pass


hotel = CRUDHotel(Hotel)

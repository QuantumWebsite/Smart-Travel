from app.crud.base import CRUDBase
from app.models.weather import Weather
from app.schemas.base_schema import DefaultCreate, DefaultUpdate


class CRUDWeather(CRUDBase[Weather, DefaultCreate, DefaultUpdate]):
    pass


weather = CRUDWeather(Weather)

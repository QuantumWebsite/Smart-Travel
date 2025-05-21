from app.crud.base import CRUDBase
from app.models.notification import Notification
from app.schemas.base_schema import DefaultCreate, DefaultUpdate


class CRUDNotification(CRUDBase[Notification, DefaultCreate, DefaultUpdate]):
    """
    CRUD operations for Notification
    """
    pass


notification = CRUDNotification(Notification)

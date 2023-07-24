from datetime import datetime

from app.repositories.base import BaseRepository
from app.db.models import NotificationModel


class Notification(BaseRepository):
    @staticmethod
    def list_waiting_get(current_datetime: datetime):
        notifications = NotificationModel.select().where(
            (NotificationModel.state == "waiting") & (NotificationModel.datetime <= current_datetime)
        ).execute()
        return notifications

from datetime import datetime, timezone

from app.repositories.base import BaseRepository
from app.db.models import NotificationModel


class Notification(BaseRepository):
    @staticmethod
    def list_waiting_get(current_datetime: datetime):
        utc_current_datetime = current_datetime.astimezone(timezone.utc)
        notifications = NotificationModel.select().where(
            (NotificationModel.state == "waiting") & (NotificationModel.datetime <= utc_current_datetime)
        ).execute()
        return notifications

from peewee import PrimaryKeyField, ForeignKeyField

from app.db.models.base import BaseModel
from app.db.models.notification import Notification
from app.db.models.user import User


class NotificationUser(BaseModel):
    id = PrimaryKeyField()
    notification = ForeignKeyField(model=Notification, on_delete='cascade', backref='tags')
    user = ForeignKeyField(model=User, on_delete='cascade', backref='tags')

    class Meta:
        db_table = 'notifications_users'

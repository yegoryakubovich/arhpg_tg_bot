from peewee import PrimaryKeyField, CharField, ForeignKeyField, DateTimeField

from app.db.models.base import BaseModel
from app.db.models.notification import Notification
from app.db.models.user import User


class NotificationReport(BaseModel):
    id = PrimaryKeyField()
    notification = ForeignKeyField(model=Notification, on_delete='cascade', backref='tags')
    user = ForeignKeyField(model=User, on_delete='cascade', backref='tags')
    state = CharField(max_length=16)
    datetime = DateTimeField()

    class Meta:
        db_table = 'notifications_reports'

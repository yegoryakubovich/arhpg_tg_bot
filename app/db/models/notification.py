from peewee import PrimaryKeyField, CharField, DateTimeField

from app.db.models.base import BaseModel


class Notification(BaseModel):
    id = PrimaryKeyField()
    text = CharField(max_length=4096)
    datetime = DateTimeField(null=True, default=None)
    state = CharField(max_length=16)

    class Meta:
        db_table = 'notifications'

from peewee import PrimaryKeyField, CharField

from app.db.models.base import BaseModel


class Setting(BaseModel):
    id = PrimaryKeyField()
    key = CharField(max_length=256)
    value = CharField(max_length=256)

    class Meta:
        db_table = 'settings'

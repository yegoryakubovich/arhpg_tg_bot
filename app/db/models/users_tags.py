from peewee import PrimaryKeyField, CharField

from app.db.models.base import BaseModel


class UserTag(BaseModel):
    id = PrimaryKeyField()
    tag_id = CharField(max_length=128)
    name = CharField(max_length=128)
    title = CharField(max_length=128)

    class Meta:
        db_table = 'users_tags'

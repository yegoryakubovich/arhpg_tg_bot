from peewee import PrimaryKeyField, CharField, ForeignKeyField

from app.db.models.base import BaseModel
from app.db.models.category_text import CategoryText


class Text(BaseModel):
    id = PrimaryKeyField()
    category = ForeignKeyField(model=CategoryText)
    key = CharField(max_length=256)
    value = CharField(max_length=8192)

    class Meta:
        db_table = 'texts'

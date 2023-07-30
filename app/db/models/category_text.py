from peewee import PrimaryKeyField, CharField

from app.db.models.base import BaseModel


class CategoryText(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=16)

    class Meta:
        db_table = 'categories_texts'

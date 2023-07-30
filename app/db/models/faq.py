from peewee import PrimaryKeyField, CharField, IntegerField

from app.db.models.base import BaseModel


class Faq(BaseModel):
    id = PrimaryKeyField()
    priority = IntegerField()
    type = CharField(max_length=8)
    question = CharField(max_length=2048)
    answer_button = CharField(max_length=2048)

    class Meta:
        db_table = 'faqs'

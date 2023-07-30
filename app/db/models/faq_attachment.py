from peewee import PrimaryKeyField, CharField, ForeignKeyField

from app.db.models.base import BaseModel
from app.db.models.faq import Faq


class FaqAttachment(BaseModel):
    id = PrimaryKeyField()
    faq = ForeignKeyField(model=Faq, on_delete='cascade', backref='attachments')
    type = CharField(max_length=8)
    value = CharField(max_length=4096)

    class Meta:
        db_table = 'faqs_attachments'

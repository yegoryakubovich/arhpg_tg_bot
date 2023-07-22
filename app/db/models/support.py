from peewee import PrimaryKeyField, BigIntegerField, CharField

from app.db.models.base import BaseModel


class SupportUsedesk(BaseModel):
    id = PrimaryKeyField()
    tg_user_id = BigIntegerField()
    ticket_id = CharField(max_length=256)
    status = CharField(max_length=8192)

    class Meta:
        db_table = 'supports_usedesks'

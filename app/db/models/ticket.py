from peewee import PrimaryKeyField, CharField, ForeignKeyField, BigIntegerField

from app.db.models.base import BaseModel
from app.db.models.user import User


class Ticket(BaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(model=User, backref='tickets')
    ticket_id = BigIntegerField()
    state = CharField(max_length=16)

    class Meta:
        db_table = 'tickets'

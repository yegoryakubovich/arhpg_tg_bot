from peewee import PrimaryKeyField, BigIntegerField, CharField

from app.db.models.base import BaseModel


class User(BaseModel):
    id = PrimaryKeyField()
    arhpg_id = BigIntegerField()
    arhpg_token = CharField(max_length=1024)
    tg_user_id = BigIntegerField()
    firstname = CharField(max_length=128, null=True)
    lastname = CharField(max_length=128, null=True)
    email = CharField(max_length=256, null=True)

    class Meta:
        db_table = 'users'

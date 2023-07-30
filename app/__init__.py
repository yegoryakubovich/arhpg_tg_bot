
from app.aiogram import bot_create, dp

from app.db import tables_create
from app.utils.notificator import notificator_create


def app_create():
    tables_create()
    notificator_create()
    bot_create()


from aiogram import Bot

from config import TG_BOT_TOKEN


def bot_get():
    bot = Bot(
        token=TG_BOT_TOKEN,
    )
    return bot

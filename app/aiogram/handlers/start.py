from aiogram import types

from app.aiogram.kbs import Kbs
from app.aiogram.states import States
from app.db.manager import db_manager
from app.repositories import Text
from app.utils.decorators import user_get


@db_manager
@user_get
async def handler_start(message: types.Message, user):
    await States.menu.set()
    await message.reply(text=Text.get('menu'), reply_markup=await Kbs.menu())

from aiogram import types

from app.aiogram.kbs import Kbs
from app.aiogram.states import States
from app.db.manager import db_manager
from app.repositories import Text
from app.utils.decorators import user_get


@db_manager
@user_get
async def handler_program(message: types.Message, user):
    from app.aiogram.handlers import handler_program_user
    from app.aiogram.handlers import handler_general_programs
    text = message.text

    if text == Text.get('user_programs'):
        await handler_program_user(message, user)
    elif text == Text.get('general_programs'):
        await handler_general_programs(message, user)
    elif text == Text.get('back'):
        await States.menu.set()
        await message.reply(text=Text.get('menu'), reply_markup=await Kbs.menu())
    else:
        await message.reply(text=Text.get('error'))

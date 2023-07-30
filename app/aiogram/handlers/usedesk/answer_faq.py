from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.aiogram.states import States
from app.db.manager import db_manager
from app.repositories import Text
from app.utils.decorators import user_get


@db_manager
@user_get
async def handler_support_usedesk_button(callback_query: types.CallbackQuery, user):
    await States.support.set()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(Text.get('back')))
    await callback_query.message.reply(text=Text.get('text_supports'), reply_markup=keyboard)

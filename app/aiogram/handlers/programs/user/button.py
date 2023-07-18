import requests

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.db.manager import db_manager
from app.repositories import Text
from app.utils.decorators import user_get
from app.utils.decorators.programs import get_upcoming_events


@db_manager
@user_get
async def handler_program_user(message: Message, user):
    events = await get_upcoming_events(user.id, max_events=5)
    if not events:
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(text=Text.get('entry_programs'), url="ссылка_на_платформу")
        )
        await message.answer(text=Text.get('error_not_programs'), reply_markup=keyboard)
        return

    event_list_text = "В ближайшее время у вас:\n"
    for event in events:
        event_title = event.get('event_title')
        place_title = event.get('place', {}).get('title')
        event_list_text += f"[{Text.get('name_programs')} {event_title}, {Text.get('place_programs')} {place_title}]\n"

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text=Text.get('full_programs'), url="ссылка_на_платформу"),
        InlineKeyboardButton(text=Text.get('return_back'), callback_data='return_back')
    )

    await message.answer(event_list_text, reply_markup=keyboard)

from datetime import datetime

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.db.manager import db_manager
from app.repositories import Text
from app.utils.api_client import api_client
from app.utils.decorators import user_get


@db_manager
@user_get
async def handler_general_programs(message: Message, user):
    date = "2021-11-11"
    events = await api_client.xle.get_events(date, json_response=True)

    if 'status' in events and events['status'] == 404:
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(text=Text.get('entry_programs'), url="https://www.google.de")
        )
        await message.answer(text=Text.get('error_not_programs'), reply_markup=keyboard)
        return

    events_for_date = [event for event in events if event.get('date') == date]

    event_list_text = f"Мероприятия на {date}:\n"
    for event in events_for_date:
        event_title = event.get('title')
        place_title = event.get('place', {}).get('title')
        event_list_text += f"[{Text.get('name_programs')} {event_title}, {Text.get('place_programs')} {place_title}]\n"

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text=Text.get('full_programs'), url="https://www.google.de"))

    await message.answer(event_list_text, reply_markup=keyboard)

from datetime import datetime

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.db.manager import db_manager
from app.repositories import Text
from app.utils.api_client import api_client
from app.utils.decorators import user_get


@db_manager
@user_get
async def handler_program_user(message: Message, user):
    now = datetime.now()
    target_date = now.strftime('%Y-%m-%d')
    arhpg_id = user.arhpg_id
    events = await api_client.xle.get_user_events(arhpg_id, target_date)

    if not events:
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(text=Text.get('entry_programs'), url="https://www.google.de/")
        )
        await message.answer(text=Text.get('error_not_programs'), reply_markup=keyboard)
        return

    upcoming_events = [event for event in events if event['date'] > now]
    sorted_upcoming_events = sorted(upcoming_events, key=lambda x: x['date'])
    events = sorted_upcoming_events[:5]

    event_list_text = "В ближайшее время у вас:\n"
    for event in events:
        event_title = event.get('event_title')
        place_title = event.get('place', 'title')
        event_list_text += f"{Text.get('name_programs')} {event_title}," \
                           f"{Text.get('place_programs')} {place_title}\n"

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text=Text.get('full_programs'), url="https://www.google.de/"),
    )

    await message.answer(event_list_text, reply_markup=keyboard)

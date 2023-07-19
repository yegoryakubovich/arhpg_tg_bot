from datetime import datetime

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.db.manager import db_manager
from app.repositories import Text
from app.utils.api_client import api_client
from app.utils.decorators import user_get
from config import ALL_PROGRAMS


@db_manager
@user_get
async def handler_program_user(message: Message, user):
    now = datetime.now()
    target_date = now.strftime('%Y-%m-%d')
    arhpg_id = user.arhpg_id
    events = await api_client.xle.get_user_events(arhpg_id, target_date)

    if not events:
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(text=Text.get('entry_programs'), url=ALL_PROGRAMS)
        )
        await message.answer(text=Text.get('error_not_programs'), reply_markup=keyboard)
        return

    upcoming_events = [event for event in events if event['date'] > now and event.get('status') == 'running']
    sorted_upcoming_events = sorted(upcoming_events, key=lambda x: x['date'])
    events = sorted_upcoming_events[:5]

    event_list_text = "В ближайшее время у вас:\n"
    keyboard = InlineKeyboardMarkup(row_width=2)

    for event in events:
        event_title = event.get('event_title')
        place_title = event.get('place', 'title')
        event_uuid = event.get('event_uuid')
        event_list_text += f"{Text.get('name_programs')} {event_title}," \
                           f"{Text.get('place_programs')} {place_title}\n"

        if event_uuid:
            event_link = await api_client.xle.oauth_url_create(event_uuid)
            keyboard.add(InlineKeyboardButton(text=Text.get('full_programs'), url=event_link))

    await message.answer(event_list_text, reply_markup=keyboard)
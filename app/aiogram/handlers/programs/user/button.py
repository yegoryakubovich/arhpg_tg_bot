from datetime import datetime, timedelta

import pytz
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.db.manager import db_manager
from app.repositories import Text
from app.utils.api_client import api_client
from app.utils.decorators import user_get
from config import URL_ALL_PROGRAMS, URL_PROGRAM


@db_manager
@user_get
async def handler_program_user(message: Message, user):
    now = datetime.now(pytz.timezone('Europe/Moscow')).date()
    five_days_later = now + timedelta(days=5)
    arhpg_id = user.arhpg_id
    events = await api_client.xle.get_user_events(arhpg_id, now.strftime('%Y-%m-%d'))
    if not events:
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(text=Text.get('entry_programs'), url=URL_ALL_PROGRAMS)
        )
        await message.answer(text=Text.get('error_not_programs'), reply_markup=keyboard)
        return

    keyboard = InlineKeyboardMarkup(row_width=2)
    for event in events:
        status = event.get('status')
        event_date_str = event.get('start_dt')
        event_date = datetime.fromisoformat(event_date_str.replace('Z', '+00:00')).date()

        if status in ['planned', 'running'] and now <= event_date <= five_days_later:
            event_title = event.get('title')
            event_place_title = event['place'].get('title')
            event_text = f"{event_title}\n{event_place_title}"

            event_uuid = event.get('event_uuid')
            if event_uuid:
                event_url = f"{URL_PROGRAM}{event_uuid}"
                keyboard.add(InlineKeyboardButton(text=event_text, url=event_url))

    if keyboard.inline_keyboard:
        keyboard.add(InlineKeyboardButton(text=Text.get('full_programs'), url=URL_ALL_PROGRAMS))
        await message.answer(text=Text.get('shortly_user_programs'), reply_markup=keyboard)
    else:
        await message.answer(text=Text.get('error_not_programs'))

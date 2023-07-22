#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from datetime import datetime


import pytz
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.db.manager import db_manager
from app.repositories import Text

from app.utils.decorators import user_get
from app.utils.programs import format_event_text, get_upcoming_events
from config import URL_PROGRAM


@db_manager
@user_get
async def handler_general_programs(message: Message, user):
    tz = pytz.timezone('Europe/Moscow')
    now = datetime.now()
    selected_date_str = message.get_args()
    if selected_date_str:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    else:
        now = datetime.now(tz)
        selected_date = now.date()

    selected_datetime = tz.localize(datetime.combine(selected_date, datetime.min.time()))

    upcoming_events = await get_upcoming_events(selected_datetime)

    if not upcoming_events:
        await message.reply(text=Text.get('shortly_not_programs'))
        return

    keyboard = InlineKeyboardMarkup(row_width=1)

    for event in upcoming_events[:3]:
        event_text = format_event_text(event)
        event_uuid = event.get('event_uuid')
        if event_uuid:
            event_url = f"{URL_PROGRAM}{event_uuid}"
            keyboard.add(InlineKeyboardButton(text=event_text, url=event_url))

    if keyboard.inline_keyboard:
        await message.answer(text=Text.get('shortly_full_programs'), reply_markup=keyboard)
    else:
        await message.answer(text=Text.get('error_not_programs'))
        return

    keyboard_buttons = []

    current_date_found = False
    for event in upcoming_events:
        event_start_datetime = tz.localize(datetime.fromisoformat(event['start_dt'][:-6]))
        if event_start_datetime > tz.localize(datetime.now()):
            current_date_found = True
            break

    if not current_date_found and len(upcoming_events) > 2:
        if selected_date > now.date():
            keyboard_buttons.append(("Раньше", f"earlier_{selected_date}"))
        if selected_date < upcoming_events[-1]['start_dt']:
            keyboard_buttons.append(("Позже", f"later_{selected_date}"))

    keyboard_buttons.append(("Выбрать дату", "select_date"))

    keyboard = InlineKeyboardMarkup(row_width=2)
    for text, callback_data in keyboard_buttons:
        keyboard.add(InlineKeyboardButton(text=text, callback_data=callback_data))

    await message.answer(text='Выберите действие', reply_markup=keyboard)

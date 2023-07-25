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
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.aiogram.callback_datas import program_callback_data
from app.repositories import Text
from app.repositories.setting import Setting
from app.utils.api_client import api_client
from config import URL_PROGRAM, URL_ALL_PROGRAM


async def events_get(datetime_selected: datetime, page=1):
    events_in_request = await Setting.events_in_request() * page

    events = await api_client.xle.get_events(
        start_date=datetime_selected.strftime('%Y-%m-%d'),
        events_in_request=events_in_request,
    )

    # Максимальное количество МП
    events_count = await Setting.events_count()

    message = Text.get(key='shortly_full_programs') + '\n\n'
    keyboard = InlineKeyboardMarkup(row_width=2)

    event_current = 0
    datetime_current = datetime.now(pytz.timezone('Europe/Moscow'))

    for event in events:
        event_datetime_start_str = event.get('start_dt')
        if not event_datetime_start_str:
            continue

        event_datetime_start = datetime.fromisoformat(event_datetime_start_str.replace('Z', '+00:00'))

        if event_datetime_start < datetime_current:
            continue

        event_datetime_end_str = event.get('end_dt')
        if not event_datetime_end_str:
            continue

        event_current += 1
        if event_current < events_count * page - events_count + 1:
            continue

        event_datetime_end = datetime.fromisoformat(event_datetime_end_str[:-6])
        event_title = event.get('title')
        event_uuid = event.get('event_uuid')
        event_url = f'{URL_PROGRAM}{event_uuid}'

        message += f'{event_current}. {event_datetime_start.strftime("%d.%m %H:%M")} - ' \
                   f'{event_datetime_end.strftime("%H:%M")} ' \
                   f'{event_title}\n'
        keyboard.add(InlineKeyboardButton(
            text=f'{event_current}. {event_title}',
            url=event_url,
        ))

        if event_current >= events_count * page:
            break

    button_previews = InlineKeyboardButton(
        text=Text.get(key='earlier'),
        callback_data=program_callback_data.new(
            datetime_selected=datetime_selected.strftime('%Y-%m-%d'),
            page=1 if page == 1 else page-1,
        ),
    )

    button_next = InlineKeyboardButton(
        text=Text.get(key='later'),
        callback_data=program_callback_data.new(
            datetime_selected=datetime_selected.strftime('%Y-%m-%d'),
            page=events_count if page == 5 else page+1,
        ),
    )

    buttons = []

    if page > 1:
        buttons.append(button_previews)
    if page < 5 and event_current == events_count * page:
        buttons.append(button_next)

    keyboard.row(*buttons)
    keyboard.add(InlineKeyboardButton(
        text=Text.get('full_programs'),
        url=URL_ALL_PROGRAM,
    ))

    if event_current == 0:
        message = Text.get(key='shortly_not_programs')

    return message, keyboard

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


from datetime import datetime, timedelta

import pytz
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.repositories import Text
from app.repositories.setting import Setting
from app.utils.api_client import api_client
from config import URL_PROGRAM, URL_ALL_PROGRAM


async def events_get(datetime_selected: datetime):
    events = await api_client.xle.get_events(datetime_selected.strftime('%Y-%m-%d'))

    # Максимальное количество МП
    events_count = await Setting.events_count()

    message = Text.get(key='planned_day_programs') + '\n\n'
    keyboard = InlineKeyboardMarkup(row_width=2)

    event_current = 1
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

        event_datetime_end = datetime.fromisoformat(event_datetime_end_str[:-6])
        event_title = event.get('title')[:24]
        event_uuid = event.get('event_uuid')
        event_url = f'{URL_PROGRAM}{event_uuid}'

        message += f'{event_current}. {event_datetime_start.strftime("%d.%m %H:%M")} - ' \
                   f'{event_datetime_end.strftime("%H:%M")} ' \
                   f'{event_title}'
        keyboard.add(InlineKeyboardButton(
            text=f'{event_current}. {event_title}',
            url=event_url,
        ))

        event_current += 1
        if event_current > events_count:
            break

    datetime_previews = datetime_selected - timedelta(days=1)
    datetime_next = datetime_selected + timedelta(days=1)

    button_previews = InlineKeyboardButton(
        text=Text.get(key='earlier'),
        callback_data='programs_' + datetime_previews.strftime('%Y-%m-%d'),
    )
    button_next = InlineKeyboardButton(
        text=Text.get(key='later'),
        callback_data='programs_' + datetime_next.strftime('%Y-%m-%d'),
    )
    button_date = InlineKeyboardButton(
        text=Text.get(key='choose_date'),
        callback_data='programs_date_select_{}'.format(datetime_current.strftime('%Y-%m-%d')),
    )

    keyboard.row(button_previews, button_date, button_next)
    keyboard.add(InlineKeyboardButton(
        text=Text.get('full_programs'),
        url=URL_ALL_PROGRAM,
    ))

    return message, keyboard

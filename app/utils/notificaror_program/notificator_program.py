#
# (c) 2023, Yegor Yakubovich
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

from app.aiogram import bot_get
from app.db.manager import db_manager
from app.repositories import Text
from app.utils.api_client import api_client
from app.utils.decorators import user_get
from config import URL_PROGRAM

bot = bot_get()


@user_get
@db_manager
async def notificator_program(user):
    now = datetime.now(pytz.timezone('Europe/Moscow')).date()
    arhpg_id = user.arhpg_id
    events = await api_client.xle.get_user_all_events(arhpg_id, now.strftime('%Y-%m-%d'))
    print(events)

    keyboard = InlineKeyboardMarkup(row_width=2)
    notification_text = Text.get('good_morning')

    for event in events:
        event_title = event.get('title')
        event_place_title = event['place'].get('title')
        event_text = f"{event_title}\n{event_place_title}"

        event_uuid = event.get('event_uuid')
        if event_uuid:
            event_url = f"{URL_PROGRAM}{event_uuid}"
            keyboard.add(InlineKeyboardButton(text=event_text, url=event_url))

    notification_text += Text.get('desire')
    await api_client.send_message(user.tg_user_id, notification_text, reply_markup=keyboard)

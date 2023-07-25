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

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytz import timezone

from app.aiogram.kbs import Kbs
from app.aiogram.states import States
from app.db.manager import db_manager
from app.repositories import Text
from app.utils.api_client import api_client
from app.utils.decorators import user_get
from app.utils.events_get import events_get
from config import URL_PROGRAM, URL_ALL_PROGRAM


tz = timezone('Europe/Moscow')


@db_manager
@user_get
async def handler_program(message: types.Message, user):
    text = message.text

    if text == Text.get('user_programs'):
        now = datetime.now(tz=tz).date()
        five_days_later = now + timedelta(days=2)
        arhpg_id = user.arhpg_id
        events = await api_client.xle.get_user_events(arhpg_id, now.strftime('%Y-%m-%d'))

        keyboard = InlineKeyboardMarkup(row_width=2)
        counter = 0

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
                    counter += 1

                if counter >= 5:
                    break

        if counter == 0:
            keyboard = InlineKeyboardMarkup().add(
                InlineKeyboardButton(text=Text.get('entry_programs'), url=URL_ALL_PROGRAM)
            )
            await message.answer(text=Text.get('error_not_programs'), reply_markup=keyboard)
            return

        if keyboard.inline_keyboard:
            keyboard.add(InlineKeyboardButton(text=Text.get('full_programs'), url=URL_ALL_PROGRAM))
            await message.answer(text=Text.get('shortly_user_programs'), reply_markup=keyboard)

    elif text == Text.get('general_programs'):
        text, keyboard = await events_get(datetime_selected=datetime.now(tz=tz))
        await message.answer(text=text, reply_markup=keyboard)
    elif text == Text.get('back'):
        await States.menu.set()
        await message.reply(text=Text.get('menu'), reply_markup=await Kbs.menu())
    else:
        await message.reply(text=Text.get('error'))

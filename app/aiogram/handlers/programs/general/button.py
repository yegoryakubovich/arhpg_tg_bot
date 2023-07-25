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

from pytz import timezone
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from app.aiogram.callback_datas import program_callback_data
from app.db.manager import db_manager
from app.repositories import Text
from app.utils.decorators import user_get
from app.utils.events_get import events_get


tz = timezone('Europe/Moscow')
MONTHS = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноябрь',
    12: 'декабрь'
}
DAYS = {
    1: 'Понедельник',
    2: 'Вторник',
    3: 'Среда',
    4: 'Четверг',
    5: 'Пятница',
    6: 'Суббота',
    7: 'Воскресенье',
}


@db_manager
@user_get
async def handler_general_programs_button(callback_query: CallbackQuery, user):
    data = program_callback_data.parse(callback_query.data)
    datetime_selected = datetime.strptime(data['datetime_selected'], '%Y-%m-%d')
    page = int(data['page'])

    text, keyboard = await events_get(
        datetime_selected=datetime_selected,
        page=page,
    )

    await callback_query.message.edit_text(text=text)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)

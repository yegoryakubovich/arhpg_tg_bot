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


from aiogram import types


from app.db.manager import db_manager
from app.utils.decorators import user_get


@db_manager
@user_get
async def handler_programs_button(callback_query: types.CallbackQuery, user, arhpg_id, arhpg_token):
    url = f"https://api.example.com/user/{arhpg_id}?app_token={arhpg_token}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Здесь нужно обработать полученные данные из API
        # Предположим API возвращает список мероприятий с ключом "events"
        events = data.get("events", [])

        if not events:
            await callback_query.answer("У вас нет доступных мероприятий.")
            return

        max_events_to_show = min(len(events), 5)
        message_text = "В ближайшее время у вас:\n"
        buttons = []

        for index, event in enumerate(events[:max_events_to_show], start=1):
            # Это наверно инфу в текста запихивать или базу создавать с текстомо мероприятии, ну наверное в админке это
            direction = event.get("direction", "информации о направлении")
            name = event.get("name", "информации о названии")
            location = event.get("location", "Место проведения ")
            event_info = f"{direction}, {name}, {location}"

            event_link = event.get("link", "https://example.com")
            button = types.InlineKeyboardButton(f"[мероприятие {index}] {event_info}", url=event_link)

            buttons.append(button)

        buttons.append(types.InlineKeyboardButton("Посмотреть полную программу",
                                                  url="https://example.com/полная_программа"))
        buttons.append(types.InlineKeyboardButton("Вернуться назад",
                                                  callback_data="back_to_program"))

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)

        await callback_query.message.answer(message_text, reply_markup=keyboard)
    else:
        await callback_query.answer("Ошибка при получении данных с сервера.")

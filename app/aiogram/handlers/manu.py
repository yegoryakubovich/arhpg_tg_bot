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
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.db.manager import db_manager
from app.repositories import Text
from app.utils.decorators import user_get


@db_manager
@user_get
async def handler_menu(message: types.Message, user):
    welcome_message = Text.get('menu')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(text=Text.get('menu_program')),
        KeyboardButton(text=Text.get('menu_faqs')),
        KeyboardButton(text=Text.get('menu_support'))
    )

    await message.reply(welcome_message, reply_markup=keyboard)

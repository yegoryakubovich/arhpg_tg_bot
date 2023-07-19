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


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.repositories import Text


class Kbs:
    @staticmethod
    async def back():
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton(text=Text.get('back')))
        return kb

    @staticmethod
    async def menu():
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton(text=Text.get('menu_program')))
        kb.add(KeyboardButton(text=Text.get('menu_faqs')))
        kb.add(KeyboardButton(text=Text.get('menu_support')))
        return kb

    @staticmethod
    async def programs():
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton(text=Text.get('user_programs')))
        kb.add(KeyboardButton(text=Text.get('general_programs')))
        kb.add(KeyboardButton(text=Text.get('back')))
        return kb

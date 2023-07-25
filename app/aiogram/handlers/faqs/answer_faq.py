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
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.db.manager import db_manager
from app.repositories import Faq, FaqTypes, Text
from app.utils.decorators import user_get


@db_manager
@user_get
async def handler_answer_faqs(callback_query: types.CallbackQuery, user):
    await callback_query.message.reply(text=Text.get('faqs'))

    for faq in Faq.list_get():
        keyboard = InlineKeyboardMarkup(row_width=1)
        button = InlineKeyboardButton(
            text=faq.answer_button,
        )

        if faq.type == FaqTypes.url:
            button.url = faq.attachments[0].value
        elif faq.type == FaqTypes.text:
            button.callback_data = f'faqs_{faq.id}'
        keyboard.add(button)

        await callback_query.bot.send_message(chat_id=callback_query.message.chat.id,
                                              text=faq.question, reply_markup=keyboard)

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

from app.aiogram.kbs import Kbs
from app.aiogram.states import States
from app.db.manager import db_manager
from app.db.models import FaqAttachment, Faq
from app.repositories import Text
from app.utils.decorators import user_get


@db_manager
@user_get
async def handler_faqs(message: types.Message, user):
    text = message.text

    if text == Text.get('back'):
        await States.menu.set()
        await message.reply(text=Text.get('menu'), reply_markup=await Kbs.menu())
    else:
        await message.reply(text=Text.get('error'))


@db_manager
@user_get
async def handle_text_button(callback_query: types.CallbackQuery):
    data = callback_query.data.split(':')
    if len(data) == 2 and data[0] == 'faq_attachment':
        attachment_id = data[1]
        attachment = FaqAttachment.get_or_none(id=attachment_id)

        if attachment and attachment.type == 'text':
            await callback_query.bot.send_message(chat_id=callback_query.message.chat.id, text=attachment.value)


@db_manager
@user_get
async def display_faqs(message: types.Message, user):
    faqs = Faq.select()

    for faq in faqs:
        attachments = FaqAttachment.select().where(FaqAttachment.faq == faq)
        keyboard = InlineKeyboardMarkup(row_width=1)

        for attachment in attachments:
            if attachment.type == 'url':
                button = InlineKeyboardButton(
                    text=faq.answer_button, url=attachment.value)
            elif attachment.type == 'text':
                button = InlineKeyboardButton(
                    text=faq.answer_button, callback_data=f"faq_attachment:{attachment.id}")
            else:
                continue

            keyboard.add(button)

        await message.bot.send_message(chat_id=message.chat.id, text=faq.question, reply_markup=keyboard)

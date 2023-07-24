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


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, Message, ReplyKeyboardMarkup
from app.aiogram.states import States
from app.db.manager import db_manager
from app.repositories import Text, Faq, FaqTypes
from app.utils.decorators import user_get


@db_manager
@user_get
async def handler_menu(message: Message, user):
    text = message.text

    if text == Text.get('menu_program'):
        await States.programs.set()
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            KeyboardButton(Text.get('user_programs')),
            KeyboardButton(Text.get('general_programs')),
        )
        keyboard.add(KeyboardButton(Text.get('back')))
        await message.reply(text=Text.get('program'), reply_markup=keyboard)

    elif text == Text.get('menu_faqs'):
        await message.reply(text=Text.get('faqs'))

        for faq in Faq.list_get():
            keyboard = InlineKeyboardMarkup(row_width=1)
            button = InlineKeyboardButton(
                text=faq.answer_button,
            )

            if faq.type == FaqTypes.url:
                button.url = faq.attachments[0].value
            elif faq.type == FaqTypes.text:
                button.callback_data = 'faqs_{faq_id}'.format(
                    faq_id=faq.id,
                )
            keyboard.add(button)

            await message.bot.send_message(chat_id=message.chat.id, text=faq.question, reply_markup=keyboard)

    elif text == Text.get('menu_support'):
        await States.support.set()
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton(Text.get('back')))
        await message.reply(text=Text.get('text_supports'), reply_markup=keyboard)

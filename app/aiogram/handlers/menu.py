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


from app.aiogram.handlers.program import handler_program
from app.aiogram.handlers.support import handler_support
from app.aiogram.kbs import Kbs
from app.aiogram.states import States
from app.db.manager import db_manager
from app.repositories import Text
from app.utils.decorators import user_get
from app.utils.faq import display_faqs


@db_manager
@user_get
async def handler_menu(message: types.Message, user):
    text = message.text

    if text == Text.get('menu_program'):
        await States.program.set()
        await message.reply(text=Text.get('program'), reply_markup=await Kbs.back())
        await handler_program(message, user)
    elif text == Text.get('menu_faqs'):
        await States.faqs.set()
        await message.reply(text=Text.get('faqs'), reply_markup=await Kbs.back())
        await display_faqs(message, user)
    elif text == Text.get('menu_support'):
        await States.support.set()
        await message.reply(text=Text.get('support'), reply_markup=await Kbs.back())
        await handler_support(message, user)
    else:
        await message.reply(text=Text.get('error'), reply_markup=await Kbs.menu())

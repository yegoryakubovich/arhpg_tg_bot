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


from aiogram.types import InlineQuery, CallbackQuery

from app.db.manager import db_manager
from app.utils.decorators import user_get


@db_manager
@user_get
async def handler_faqs_button(callback_query: CallbackQuery, user):
    print(callback_query.data)
    await callback_query.message.reply('ffww')
    await callback_query.answer()

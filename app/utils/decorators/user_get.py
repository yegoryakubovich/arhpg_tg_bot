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


from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from app.repositories import User, Text
from app.utils.api_client import api_client


def user_get(function):
    async def wrapper(*args):
        message = args[0]
        message: Message

        tg_user_id = message.from_user.id
        commands = message.text.split()

        if len(commands) == 2:
            arhpg_token = commands[-1]

            sso_user = await api_client.sso.user_get(token=arhpg_token)
            arhpg_id = sso_user.get('leader_id')
            firstname = sso_user.get('firstname')
            lastname = sso_user.get('lastname')

            if arhpg_id:
                await User.create(
                    arhpg_id=arhpg_id,
                    arhpg_token=arhpg_token,
                    tg_user_id=tg_user_id,
                    firstname=firstname,
                    lastname=lastname,
                )

        is_authorized = await User.is_authorized(tg_user_id=tg_user_id)
        if not is_authorized:
            url = await api_client.sso.oauth_url_create()

            kb = InlineKeyboardMarkup(row_width=1)
            kb.add(InlineKeyboardButton(
                text=Text.get('greetings_sso_button'),
                url=url,
            ))
            return await message.reply(text=Text.get('greetings_sso'), reply_markup=kb)

        user = await User.get(tg_user_id=tg_user_id)

        kwargs = {
            'message': message,
            'user': user,
        }
        return await function(**kwargs)

    return wrapper

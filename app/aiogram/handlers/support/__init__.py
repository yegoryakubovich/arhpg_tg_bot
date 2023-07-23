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


import json

import requests
from aiogram import types

from app.aiogram.states import States
from app.db.manager import db_manager
from app.repositories import Ticket
from app.repositories.ticket import TicketStates
from app.utils.decorators import user_get
from config import USEDESK_API_TOKEN, USEDESK_HOST


@db_manager
@user_get
async def handler_support(message: types.Message, user):
    message_text = message.text
    data = {
        'api_token': USEDESK_API_TOKEN,
        'subject': 'Запрос на поддержку от пользователя',
        'message': message_text,
        'client_name': user.firstname,
        'client_email': user.email
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(f'{USEDESK_HOST}/create/ticket', headers=headers, json=data)

    if response.status_code == 200:
        status = json.loads(response.content)['status']
        ticket_id = json.loads(response.content)['ticket_id']
        await Ticket.create(
            user=user,
            message=message_text,
            state=TicketStates.waiting,
            ticket_id=ticket_id,
        )

        if status == 'success':
            await message.reply("Ваш запрос принят. Служба поддержки свяжется с вами в ближайшее время.")
            await States.menu.set()
        else:
            await message.reply("Произошла ошибка при отправке запроса в службу поддержки.")

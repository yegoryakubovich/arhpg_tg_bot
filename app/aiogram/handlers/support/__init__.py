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


import requests
from aiogram import types

from app.aiogram.kbs import Kbs
from app.aiogram.states import States
from app.db.manager import db_manager
from app.repositories import Ticket, Text
from app.repositories.ticket import TicketStates
from app.repositories.setting import Setting
from app.utils.decorators import user_get
from config import USEDESK_API_TOKEN, USEDESK_HOST




@db_manager
@user_get
async def handler_support(message: types.Message, user):
    if message.text == Text.get('back'):
        await States.menu.set()
        await message.reply(text=Text.get('menu'), reply_markup=await Kbs.menu())
        return

    if message.text:
        message_text = message.text
    elif message.photo:
        message_text = message.caption or '' or None
    else:
        await message.reply(text=Text.get('Неверный формат сообщения, отправьте фото или текст'))
        return

    ticket_user = Ticket.list_waiting_get()
    waiting_tickets_count = sum(1 for ticket in ticket_user if ticket.state == TicketStates.waiting)

    # Лимит тикетов
    if waiting_tickets_count >= await Setting.limit_ticket():
        await message.reply(text=Text.get('max_ticket'))
        return

    data = {
        'api_token': USEDESK_API_TOKEN,
        'subject': Text.get('subject_ticket'),
        'message': message_text,
        'client_name': user.firstname,
        'client_email': user.email
    }

    files = []
    if message.photo:
        photo = await message.photo[-1].download()
        with open(photo, 'rb') as photo_file:
            files.append(('files[]', (photo_file.name, photo_file, 'temp/jpeg')))

    response = requests.post(f'{USEDESK_HOST}/create/ticket', headers={}, data=data, files=files)

    if response.status_code == 200:
        status = response.json()['status']
        ticket_id = response.json()['ticket_id']
        await Ticket.create(
            user=user,
            message=message_text,
            state=TicketStates.waiting,
            ticket_id=ticket_id,
        )

        if status == 'success':
            await message.reply(text=Text.get('sent_ticket'))
        else:
            await message.reply(text=Text.get('error_ticket'))

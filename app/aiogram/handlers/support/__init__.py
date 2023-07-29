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


import os
import time

import requests
from aiogram import types

from app.aiogram.kbs import Kbs
from app.aiogram.states import States
from app.db.manager import db_manager
from app.repositories import Ticket, Text
from app.repositories.ticket import TicketStates
from app.utils.decorators import user_get
from config import USEDESK_API_TOKEN, USEDESK_HOST


@db_manager
@user_get
async def handler_support(message: types.Message, user):
    if message.text == Text.get('back'):
        await States.menu.set()
        await message.reply(text=Text.get('menu'), reply_markup=await Kbs.menu())
        return

    files = []
    if message.text:
        message_text = message.text
    elif message.photo:
        if not os.path.exists('temp'):
            os.makedirs('temp')
        max_photo = max(message.photo, key=lambda p: p.file_size)
        file_path = os.path.join('temp', f'photo_{message.from_user.id}.jpg')
        await max_photo.download(destination=file_path)
        with open(file_path, 'rb') as photo_file:
            photo_data = photo_file.read()
        files.append(('files[]', (os.path.basename(file_path), photo_data, 'image/jpeg')))
        message_text = message.caption or '(фото без комментариев)'
    elif message.document:
        if not os.path.exists('temp'):
            os.makedirs('temp')
        document = message.document
        document_file_name = document.file_name
        document_path = os.path.join('temp', document_file_name)
        await message.document.download(destination=document_path)
        with open(document_path, 'rb') as document_file:
            document_data = document_file.read()
        files.append(('files[]', (document_file_name, document_data, 'application/docx')))
        message_text = message.caption or '(файл без комментариев)'
    else:
        await message.reply(text=Text.get('error_format'))
        return

    data = {
        'api_token': USEDESK_API_TOKEN,
        'subject': Text.get('subject_ticket'),
        'message': message_text,
        'client_name': user.firstname,
        'client_email': user.email
    }

    response = requests.post(f'{USEDESK_HOST}/create/ticket', headers={}, data=data, files=files)

    if response.status_code == 200:
        response_data = response.json()
        if 'status' in response_data and response_data['status'] == 'success':
            ticket_id = response_data['ticket_id']
            await Ticket.create(
                user=user,
                message=message_text,
                state=TicketStates.waiting,
                ticket_id=ticket_id,
            )
            await message.reply(text=Text.get('sent_ticket'))
        else:
            await message.reply(text=Text.get('error_ticket'))
    else:
        await message.reply(text=Text.get('error_ticket'))

    time.sleep(2)
    for filename in os.listdir('temp'):
        file_path = os.path.join('temp', filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)

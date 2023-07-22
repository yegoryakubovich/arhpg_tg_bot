import json

import requests
from aiogram import types

from app.db.manager import db_manager
from app.db.models import SupportUsedesk
from app.utils.decorators import user_get
from config import USEDESK_API_TOKEN, USEDESK_HOST


@db_manager
@user_get
async def handler_support(message: types.Message, user):
    user_data = {
        'name': message.from_user.full_name,
        'email': f'{message.from_user.username}@telegram.bot'
    }
    message_text = message.text
    data = {
        'api_token': USEDESK_API_TOKEN,
        'subject': 'Запрос на поддержку от пользователя',
        'message': message_text,
        'client_name': user_data['name'],
        'client_email': user_data['email']
    }

    response = requests.post(f'{USEDESK_HOST}', json=data)
    if response.status_code == 200:
        status = json.loads(response.content)['status']
        ticket_id = json.loads(response.content)['ticket_id']
        support_ticket = SupportUsedesk(
            tg_user_id=message.from_user.id,
            ticket_id=ticket_id,
            status=status
        )
        support_ticket.save()

        if status == 'success':
            await message.reply("Ваш запрос принят. Служба поддержки свяжется с вами в ближайшее время.")
        else:
            await message.reply("Произошла ошибка при отправке запроса в службу поддержки.")


@db_manager
@user_get
async def update_ticket_status(message: types.Message, user, ticket_id):
    ticket = SupportUsedesk.get(ticket_id=ticket_id)
    response = requests.get(f'{USEDESK_HOST}/{ticket_id}', params={'api_token': USEDESK_API_TOKEN})
    if response.status_code == 200:
        status = json.loads(response.content)['status']
        if status != ticket.status:
            ticket.status = status
            ticket.save()
            await message.answer(
                text=f"Ответ службы поддержки: {json.loads(response.content)['last_message']['message']}")

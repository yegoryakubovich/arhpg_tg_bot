import requests
from aiogram import types

from app.db.manager import db_manager
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
    print(response.content)
    if response.status_code == 200:
        await message.reply("Ваш запрос принят. Служба поддержки свяжется с вами в ближайшее время.")
    else:
        await message.reply("Произошла ошибка при отправке запроса в службу поддержки.")
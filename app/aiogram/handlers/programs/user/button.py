import requests

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.db.manager import db_manager
from app.repositories import Text
from app.utils.decorators import user_get


EVENT_UUID = '7a715579-48fc-48a9-a63e-3362bebffd46'
APP_TOKEN = 'p4rhd9f6qjlprqi1'
BASE_API_URL = 'https://xle.u2035test.ru/api/v1/event/'


@db_manager
@user_get
async def handler_program_user(message: Message, user):
    url = f'{BASE_API_URL}{EVENT_UUID}?app_token={APP_TOKEN}'

    events = get_upcoming_events(user.id, max_events=5)
    if not events:
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(text=Text.get('entry_programs'), url="ссылка_на_платформу")
        )
        await message.answer(text=Text.get('error_not_programs'), reply_markup=keyboard)
        return

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        event_title = data.get('event_title')
        place_title = data.get('place', {}).get('title')

        message_text = (
            f"\n\n{Text.get('name_programs')} {event_title}"
            f"\n{Text.get('place_programs')} {place_title}"
        )
        await message.answer(
            message_text, reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(text=Text.get('full_programs'), url=url)
            )
        )
    else:
        await message.answer(text=Text.get('error'))

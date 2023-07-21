import locale
from datetime import datetime, timedelta


import pytz
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


from app.db.manager import db_manager
from app.repositories import Text
from app.utils.api_client import api_client
from app.utils.decorators import user_get
from app.utils.decorators.programs import format_event_text
from config import URL_PROGRAM


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


@db_manager
@user_get
async def handler_select_date(callback_query: CallbackQuery, user):
    current_datetime = datetime.now(pytz.timezone('Europe/Moscow'))
    date_list_text = "Выберите дату:\n"
    keyboard = InlineKeyboardMarkup(row_width=1)

    for i in range(5):
        next_date = current_datetime + timedelta(days=i)
        formatted_date = next_date.strftime("%Y-%m-%d")
        formatted_date_russian = next_date.strftime('%A, %d %B')
        keyboard.add(InlineKeyboardButton(text=formatted_date_russian,
                                            callback_data=f"selected_date_{formatted_date}"))

    await callback_query.message.answer(date_list_text, reply_markup=keyboard)


@db_manager
@user_get
async def handler_selected_date(callback_query: CallbackQuery, user):
    selected_date_str = callback_query.data.strip()[14:]
    selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
    all_events = await api_client.xle.get_events(selected_date_str)
    upcoming_events = []

    for event in all_events:
        event_start_dt_str = event.get('start_dt')
        if not event_start_dt_str:
            continue

        event_start_dt = datetime.fromisoformat(event_start_dt_str.replace('Z', '+00:00')).date()

        if event_start_dt == selected_date:
            upcoming_events.append(event)

    if not upcoming_events:
        await callback_query.message.answer(text=Text.get('shortly_not_programs'))
        return

    keyboard = InlineKeyboardMarkup(row_width=1)
    for event in upcoming_events[:2]:
        event_text = format_event_text(event)
        event_uuid = event.get('event_uuid')
        if event_uuid:
            event_url = f"{URL_PROGRAM}{event_uuid}"
            keyboard.add(InlineKeyboardButton(text=event_text, url=event_url))

    if len(upcoming_events) > 2:
        earlier_button = InlineKeyboardButton(text="Раньше", callback_data="earlier")
        later_button = InlineKeyboardButton(text="Позже", callback_data="later")
        keyboard.row(earlier_button, later_button)

    selected_date_button = InlineKeyboardButton(text="Выбрать дату", callback_data="select_date")
    keyboard.row(selected_date_button)

    await callback_query.message.answer(text=Text.get('planned_day_programs'), reply_markup=keyboard)
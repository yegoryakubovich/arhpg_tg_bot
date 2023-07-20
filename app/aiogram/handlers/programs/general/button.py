from datetime import datetime, timezone, timedelta

import pytz
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from app.db.manager import db_manager
from app.utils.api_client import api_client
from app.utils.decorators import user_get
from config import URL_PROGRAM


@db_manager
@user_get
async def handler_general_programs(message: Message, user, selected_date=None):
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    if selected_date is None:
        selected_date = now.date()
    all_events = await api_client.xle.get_events(selected_date.strftime('%Y-%m-%d'))
    upcoming_events = []
    current_datetime = now.astimezone(pytz.timezone('Europe/Moscow'))

    for event in all_events:
        event_start_dt_str = event.get('start_dt')
        if not event_start_dt_str:
            continue

        event_start_dt = datetime.fromisoformat(event_start_dt_str.replace('Z', '+00:00'))

        if event_start_dt >= current_datetime:
            upcoming_events.append(event)

    if not upcoming_events:
        await message.reply(text='Ближайших мероприятий нет')
        return

    await message.reply(text='Ближайшие мероприятия')

    for event in upcoming_events[:5]:
        event_title = event.get('title')
        event_start_dt = datetime.fromisoformat(event['start_dt'][:-6])
        event_end_dt = datetime.fromisoformat(event['end_dt'][:-6])
        event_place_title = event['place'].get('title')

        event_text = f"{event_start_dt.strftime('%d.%m %H:%M')} - {event_end_dt.strftime('%H:%M')}" \
                     f"\n{event_title}" \
                     f"\n{event_place_title}"

        keyboard = InlineKeyboardMarkup(row_width=1)
        event_uuid = event.get('event_uuid')
        if event_uuid:
            event_url = f"{URL_PROGRAM}{event_uuid}"
            keyboard.add(InlineKeyboardButton(text=event_text, url=event_url))
        await message.answer(event_text, reply_markup=keyboard)

    keyboard_buttons = []

    current_date_found = False
    for event in upcoming_events:
        event_start_date = datetime.fromisoformat(event['start_dt'][:-6]).date()

        if event_start_date == selected_date:
            current_date_found = True
            break

    if not current_date_found:
        keyboard_buttons.append(("Раньше", "earlier"))

    keyboard_buttons.append(("Позже", "later"))
    keyboard_buttons.append(("Выбрать дату", "select_date"))

    if len(upcoming_events) <= 5:
        keyboard_buttons.pop(0)

    keyboard = InlineKeyboardMarkup(row_width=2)
    for text, callback_data in keyboard_buttons:
        keyboard.add(InlineKeyboardButton(text=text, callback_data=callback_data))

    await message.answer("Выберите действие:", reply_markup=keyboard)


@db_manager
@user_get
async def handle_later(callback_query: CallbackQuery, user):
    current_datetime = datetime.now(timezone.utc)
    current_datetime_str = current_datetime.strftime("%Y-%m-%d")
    all_events = await api_client.xle.get_events(current_datetime_str)

    upcoming_events = []
    for event in all_events:
        event_start_dt = datetime.fromisoformat(event['start_dt'][:-6])

        if event_start_dt > current_datetime:
            upcoming_events.append(event)

    upcoming_events = sorted(upcoming_events, key=lambda x: x['start_dt'])

    if upcoming_events:
        selected_date = datetime.fromisoformat(upcoming_events[-1]['start_dt'][:-6]).date()
        await handler_general_programs(callback_query.message, callback_query.from_user, selected_date, upcoming_events[:5])
    else:
        await callback_query.answer(text="Нет ближайших мероприятий")


@db_manager
@user_get
async def handle_earlier(callback_query: CallbackQuery, user):
    current_datetime = datetime.now(timezone.utc)
    current_datetime_str = current_datetime.strftime("%Y-%m-%d")
    all_events = await api_client.xle.get_events(current_datetime_str)

    selected_date = current_datetime.date()
    upcoming_events = []
    for event in all_events:
        event_start_dt = datetime.fromisoformat(event['start_dt'][:-6])

        if event_start_dt >= selected_date:
            break

        upcoming_events.append(event)

    upcoming_events = sorted(upcoming_events, key=lambda x: x['start_dt'], reverse=True)

    await handler_general_programs(callback_query.message, callback_query.from_user, selected_date, upcoming_events[:5])


@user_get
async def handle_select_date(message: Message, user):
    current_datetime = datetime.now(timezone.utc)
    current_datetime_str = current_datetime.strftime("%Y-%m-%d")
    all_events = await api_client.xle.get_events(current_datetime_str)

    event_dates = set(event['start_dt'] for event in all_events)

    upcoming_dates = []
    for start_dt in event_dates:
        event_start_dt = datetime.fromisoformat(start_dt.replace('Z', '+00:00')).astimezone(timezone.utc)
        if event_start_dt >= current_datetime:
            upcoming_dates.append(event_start_dt.date())

    upcoming_dates = sorted(upcoming_dates)

    date_list_text = "Выберите дату:\n"
    for i, date in enumerate(upcoming_dates):
        date_list_text += f"{i+1}. {date.strftime('%A, %d %B')}\n"

    keyboard = InlineKeyboardMarkup(row_width=2)

    for i in range(5):
        date_in_5_days = current_datetime + timedelta(days=i)
        if date_in_5_days.date() not in upcoming_dates:
            break
        formatted_date = date_in_5_days.strftime("%Y-%m-%d")
        keyboard.add(InlineKeyboardButton(text=date_in_5_days.strftime('%A, %d %B'),
                                          callback_data=f"select_date:{formatted_date}"))

    await message.answer(date_list_text, reply_markup=keyboard)


@db_manager
@user_get
async def handle_selected_date(callback_query: CallbackQuery, user):
    date_str = callback_query.data.split(':')[1]
    selected_date = datetime.strptime(date_str, "%Y-%m-%d")
    await handler_general_programs(callback_query.message, callback_query.from_user, selected_date)

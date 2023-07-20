import locale
from datetime import datetime, timezone, timedelta


import pytz
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from app.db.manager import db_manager
from app.repositories import Text
from app.utils.api_client import api_client
from app.utils.decorators import user_get
from app.utils.decorators.programs import format_event_text, get_upcoming_events
from config import URL_PROGRAM


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


@db_manager
@user_get
async def handler_general_programs(message: Message, user):
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    selected_date = now.date()
    selected_datetime = datetime.combine(selected_date, datetime.min.time())

    upcoming_events = await get_upcoming_events(selected_datetime)

    if not upcoming_events:
        await message.reply(text=Text.get('shortly_not_programs'))
        return

    for event in upcoming_events[:5]:
        event_text = format_event_text(event)
        keyboard = InlineKeyboardMarkup(row_width=1)
        event_uuid = event.get('event_uuid')
        if event_uuid:
            event_url = f"{URL_PROGRAM}{event_uuid}"
            keyboard.add(InlineKeyboardButton(text=event_text, url=event_url))
        await message.answer(text=Text.get('shortly_full_programs'), reply_markup=keyboard)

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

    await message.answer(text='Выберите действие', reply_markup=keyboard)


@db_manager
@user_get
async def handle_select_date(callback_query: CallbackQuery, user):
    current_datetime = datetime.now(timezone.utc)
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
async def handle_selected_date(callback_query: CallbackQuery, user):
    selected_date_str = callback_query.data.strip()[14:]
    selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d")
    all_events = await api_client.xle.get_events(selected_date.strftime('%Y-%m-%d'))
    upcoming_events = []
    print(all_events)
    for event in all_events:
        event_start_dt_str = event.get('start_dt')
        if not event_start_dt_str:
            continue

        event_start_dt = datetime.fromisoformat(event_start_dt_str.replace('Z', '+00:00'))
        print(event_start_dt)
        print(selected_date)
        if event_start_dt == selected_date:
            upcoming_events.append(event)

    if not upcoming_events:
        await callback_query.message.answer(text=Text.get('shortly_not_programs'))
        return

    for event in upcoming_events[:5]:
        event_text = format_event_text(event)
        keyboard = InlineKeyboardMarkup(row_width=1)
        event_uuid = event.get('event_uuid')
        if event_uuid:
            event_url = f"{URL_PROGRAM}{event_uuid}"
            keyboard.add(InlineKeyboardButton(text=event_text, url=event_url))
        await callback_query.message.answer(text=Text.get('shortly_full_programs'), reply_markup=keyboard)

    keyboard_buttons = []

    current_date_found = False
    for event in upcoming_events:
        event_start_date = datetime.fromisoformat(event['start_dt'][:-6]).date()

        if event_start_date == selected_date.date():
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

    await callback_query.message.answer(text='Выберите действие', reply_markup=keyboard)


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
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

    keyboard = InlineKeyboardMarkup(row_width=1)

    for event in upcoming_events[:2]:
        event_text = format_event_text(event)
        event_uuid = event.get('event_uuid')
        if event_uuid:
            event_url = f"{URL_PROGRAM}{event_uuid}"
            keyboard.add(InlineKeyboardButton(text=event_text, url=event_url))

    if keyboard.inline_keyboard:
        await message.answer(text=Text.get('shortly_full_programs'), reply_markup=keyboard)
    else:
        await message.answer(text=Text.get('error_not_programs'))

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
    all_events = await api_client.xle.get_events(selected_date.strftime('%Y-%m-%d'))
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

    for event in upcoming_events[:5]:
        event_text = format_event_text(event)
        event_uuid = event.get('event_uuid')
        if event_uuid:
            event_url = f"{URL_PROGRAM}{event_uuid}"
            keyboard.add(InlineKeyboardButton(text=event_text, url=event_url))

    if keyboard.inline_keyboard:
        await callback_query.message.answer(text=Text.get('shortly_full_programs'), reply_markup=keyboard)
    else:
        await callback_query.message.answer(text=Text.get('error_not_programs'))

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

    # Create keyboard with buttons for each event
    keyboard = InlineKeyboardMarkup(row_width=1)
    for event in upcoming_events[:2]:
        event_text = format_event_text(event)
        event_uuid = event.get('event_uuid')
        if event_uuid:
            event_url = f"{URL_PROGRAM}{event_uuid}"
            keyboard.add(InlineKeyboardButton(text=event_text, url=event_url))

    # Add "Earlier" and "Later" buttons if there are more events
    if len(upcoming_events) > 2:
        earlier_button = InlineKeyboardButton(text="Раньше", callback_data="earlier")
        later_button = InlineKeyboardButton(text="Позже", callback_data="later")
        keyboard.row(earlier_button, later_button)

    await callback_query.message.answer(text=Text.get('shortly_user_programs'), reply_markup=keyboard)


@db_manager
@user_get
async def handler_later(callback_query: CallbackQuery, user):
    current_datetime = datetime.now(timezone.utc)
    current_datetime_str = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    all_events = await api_client.xle.get_events(current_datetime_str)

    upcoming_events = []
    for event in all_events:
        event_start_dt = pytz.timezone('Europe/Moscow').localize(datetime.fromisoformat(event['start_dt']))

        if event_start_dt > current_datetime:
            upcoming_events.append(event)

    upcoming_events = sorted(upcoming_events, key=lambda x: x['start_dt'])

    if upcoming_events:
        keyboard_buttons = [("Раньше", "earlier"), ("Выбрать дату", "select_date")]

        if len(upcoming_events) > 2:
            keyboard_buttons.append(("Позже", "later"))

        keyboard = InlineKeyboardMarkup(row_width=2)
        for text, callback_data in keyboard_buttons:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=callback_data))

        events_to_show = upcoming_events

        message_text = f"Ближайщие мероприятия:"
        for event in events_to_show:
            event_text = format_event_text(event)
            message_text += f"\n\n{event_text}"

        await callback_query.message.edit_text(text=message_text, reply_markup=keyboard)
    else:
        await callback_query.answer("Нет предстоящих мероприятий")



@db_manager
@user_get
async def handler_earlier(callback_query: CallbackQuery, user):
    current_datetime = datetime.now(timezone.utc)
    current_datetime_str = current_datetime.strftime("%Y-%m-%d")
    all_events = await api_client.xle.get_events(current_datetime_str)

    selected_date = current_datetime.date()
    upcoming_events = []
    past_events = []
    for event in all_events:
        event_start_dt = pytz.timezone('Europe/Moscow').localize(datetime.fromisoformat(event['start_dt'][:-6]))

        if event_start_dt.date() >= selected_date:
            break

        if event_start_dt < current_datetime:
            past_events.append(event)
        else:
            upcoming_events.append(event)

    past_events = sorted(past_events, key=lambda x: x['start_dt'], reverse=True)

    if past_events:
        await handler_general_programs(callback_query.message, callback_query.from_user, selected_date, past_events[:5], is_previous=True)
    else:
        await callback_query.answer("Больше нет прошлых мероприятий")
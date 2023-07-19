from datetime import datetime, timezone, timedelta

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from app.db.manager import db_manager
from app.utils.api_client import api_client
from app.utils.decorators import user_get


selected_date = None


@db_manager
@user_get
async def handler_general_programs(message: Message, user, selected_date=None):
    current_datetime = datetime.now(timezone.utc)
    current_datetime_str = current_datetime.strftime("%Y-%m-%d")
    all_events = await api_client.xle.get_events(current_datetime_str)
    upcoming_events = []

    for event in all_events:
        event_start_dt_str = event.get('start_dt')
        if not event_start_dt_str:
            continue

        event_start_dt = datetime.strptime(event_start_dt_str[:-6], "%Y-%m-%dT%H:%M:%S")

        if not selected_date:
            selected_date = current_datetime

        if event_start_dt.date() == selected_date.date() and event_start_dt >= current_datetime:
            upcoming_events.append(event)

    upcoming_events = sorted(upcoming_events, key=lambda x: x['start_dt'])

    if not upcoming_events:
        await message.reply(text='Ближайших мероприятий нет')
    else:
        await message.reply(text='Ближайшие мероприятия')

    for event in upcoming_events[:5]:
        event_title = event.get('title')
        event_start_dt = datetime.fromisoformat(event['start_dt'][:-6])
        event_end_dt = datetime.fromisoformat(event['end_dt'][:-6])
        event_uuid = event.get('event_uuid')

        if event_uuid:
            event_link = await api_client.xle.oauth_url_create(event_uuid)
        else:
            event_link = None

        event_text = f"{event_start_dt.strftime('%d.%m %H:%M')} - {event_end_dt.strftime('%H:%M')}" \
                     f"\n{event_title}"

        keyboard = InlineKeyboardMarkup(row_width=1)
        if event_link:
            keyboard.add(InlineKeyboardButton(text="Просмотреть мероприятие", url=event_link))

        await message.answer(event_text, reply_markup=keyboard)

    if len(upcoming_events) > 5:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton(text="Позже", callback_data="later"),
            InlineKeyboardButton(text="Выбрать дату", callback_data="select_date"),
            InlineKeyboardButton(text="Вернуться назад", callback_data="go_back")
        )
    else:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton(text="Выбрать дату", callback_data="select_date"),
            InlineKeyboardButton(text="Вернуться назад", callback_data="go_back")
        )

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

    await handler_general_programs(callback_query.message, callback_query.from_user, selected_date, upcoming_events[:5])

@db_manager
@user_get
async def handle_select_date(callback_query: CallbackQuery, user):
    current_datetime = datetime.now(timezone.utc)
    current_datetime_str = current_datetime.strftime("%Y-%m-%d")
    all_events = await api_client.xle.get_events(current_datetime_str)

    event_dates = set(event['start_dt'] for event in all_events)

    upcoming_dates = []
    for start_dt in event_dates:
        event_start_dt = datetime.fromisoformat(start_dt[:-6])
        if event_start_dt >= current_datetime:
            upcoming_dates.append(event_start_dt.date())

    upcoming_dates = sorted(upcoming_dates)

    date_list_text = "Выберите дату:\n"
    for i, date in enumerate(upcoming_dates):
        date_list_text += f"{i+1}. {date.strftime('%A, %d %B')}\n"

    keyboard = InlineKeyboardMarkup(row_width=2)

    for i in range(7):
        date_in_7_days = current_datetime + timedelta(days=i)
        if date_in_7_days.date() not in upcoming_dates:
            break
        formatted_date = date_in_7_days.strftime("%Y-%m-%d")
        keyboard.add(InlineKeyboardButton(text=date_in_7_days.strftime('%A, %d %B'),
                                          callback_data=f"select_date:{formatted_date}"))

    keyboard.add(InlineKeyboardButton(text="Вернуться назад", callback_data="go_back"))

    await callback_query.message.answer(date_list_text, reply_markup=keyboard)

# Функция для обработки выбранной пользователем даты
@db_manager
@user_get
async def handle_selected_date(callback_query: CallbackQuery):
    global selected_date
    date_str = callback_query.data.split('_')[1]
    selected_date = datetime.strptime(date_str, "%Y-%m-%d")
    await handler_general_programs(callback_query.message, callback_query.from_user, selected_date.date())

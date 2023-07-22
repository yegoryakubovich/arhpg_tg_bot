from datetime import datetime

import pytz

from app.utils.api_client import api_client


def format_event_text(event):
    event_title = event.get('title')
    event_start_dt = datetime.fromisoformat(event['start_dt'][:-6])
    event_end_dt = datetime.fromisoformat(event['end_dt'][:-6])
    event_place_title = event['place'].get('title')

    event_text = f'{event_start_dt.strftime("%d.%m %H:%M")} - {event_end_dt.strftime("%H:%M")}' \
                 f'\n{event_title}' \
                 f'\n{event_place_title}'

    return event_text


async def get_upcoming_events(selected_date: datetime):
    all_events = await api_client.xle.get_events(selected_date.strftime('%Y-%m-%d'))
    upcoming_events = []
    current_datetime = datetime.now(pytz.timezone('Europe/Moscow'))

    for event in all_events:
        event_start_dt_str = event.get('start_dt')
        if not event_start_dt_str:
            continue

        event_start_dt = datetime.fromisoformat(event_start_dt_str.replace('Z', '+00:00'))

        if event_start_dt >= current_datetime:
            upcoming_events.append(event)

    return upcoming_events

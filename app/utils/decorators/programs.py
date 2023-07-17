from datetime import datetime
from typing import List


# Функция получения мероприятий
"""def get_user_events(user_id: int) -> List[dict]: """


# Функция для получения ближайших мероприятий пользователя
"""def get_upcoming_events(user_id: int, max_events: int = 5) -> List[dict]:
    now = datetime.now()
    events = get_user_events(user_id)
    upcoming_events = [event for event in events if event['date'] > now]
    sorted_upcoming_events = sorted(upcoming_events, key=lambda x: x['date'])
    return sorted_upcoming_events[:max_events]"""
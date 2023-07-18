from datetime import datetime
from typing import List

from app.db.manager import db_manager
from app.repositories import User
from app.utils.api_client import api_client
from app.utils.decorators import user_get


@db_manager
@user_get
async def get_upcoming_events(tg_user_id: int, max_events: int = 5) -> List[dict]:
    now = datetime.now()
    user = await User.get(tg_user_id)
    arhpg_id = user.arhpg_id
    target_date = now.strftime('%Y-%m-%d')
    events = await api_client.get_user_events(arhpg_id, target_date)
    upcoming_events = [event for event in events if event['date'] > now]
    sorted_upcoming_events = sorted(upcoming_events, key=lambda x: x['date'])
    return sorted_upcoming_events[:max_events]

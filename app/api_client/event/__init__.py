from app.api_client.api_client_base import ApiClientBase
from config import API_EVENT_TOKEN


class ApiClientEVENT(ApiClientBase):
    async def get_events_user(self, event_id: int):
        response = await self.get(
            path=f'timetable/api/v1/events/{event_id}/signed-users',
            parameters={
                'app_token': API_EVENT_TOKEN,
            },
        )
        users = response.get('payload', [])
        return users

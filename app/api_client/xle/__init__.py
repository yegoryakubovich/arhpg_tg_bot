from datetime import datetime, timedelta

from app.api_client.api_client_base import ApiClientBase, RequestTypes
from config import API_XLE_CONTEXT, API_XLE_TOKEN


class ApiClientXLE(ApiClientBase):
    async def get_user_events(self, arhpg_id: int, start_date: str):
        events = []
        for days_delta in range(5):
            date = (datetime.fromisoformat(start_date) + timedelta(days=days_delta)).date()
            response = await self.get(
                path=f'/api/v1/timetable/user/{arhpg_id}',
                parameters={
                    'app_token': API_XLE_TOKEN,
                    'context': API_XLE_CONTEXT,
                    'date': date.strftime('%Y-%m-%d')
                },
            )
            events.extend(response)
        return events

    async def get_events(self, start_date: str):
        events = []
        for days_delta in range(10):
            date = (datetime.fromisoformat(start_date) + timedelta(days=days_delta)).date()
            response = await self.get(
                path=f'/api/v1/timetable/all',
                parameters={
                    'app_token': API_XLE_TOKEN,
                    'context': API_XLE_CONTEXT,
                    'date': date.strftime('%Y-%m-%d')
                },
            )
            events.extend(response)
        return events

    async def oauth_url_create(self, event_uuid):
        url = await self.url_create(
            path=f'/api/v1/event/{event_uuid}',
            parameters={
                'app_token': API_XLE_TOKEN,
            },
        )
        return url

    async def get(self, path: str, parameters=None, token: str = None):
        if parameters is None:
            parameters = {}
        response = await self.request(
            type=RequestTypes.get,
            path=path,
            token=token,
            parameters=parameters,
        )

        return response

    async def get_fake_events(self):
        start_date = datetime(2023, 7, 21)
        upcoming_events = []

        for days_delta in range(5):
            date = start_date + timedelta(days=days_delta)
            for i in range(2):
                fake_event = {
                    'start_dt': (date + timedelta(hours=10)).isoformat() + '+03:00',
                    'title': f'Фиктивное мероприятие {i + 1} {date.strftime("%Y-%m-%d")}',
                    'description': 'Описание фиктивного мероприятия',
                    'location': 'Место проведения фиктивного мероприятия'
                }
                upcoming_events.append(fake_event)

        return upcoming_events
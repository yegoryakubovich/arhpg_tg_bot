from datetime import datetime, timedelta

from app.api_client.api_client_base import ApiClientBase, RequestTypes
from app.repositories.setting import Setting
from config import API_XLE_CONTEXT, API_XLE_TOKEN


class ApiClientXLE(ApiClientBase):
    async def get_user_events(self, arhpg_id: int, start_date: str):
        events = []
        for days_delta in range(2):
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

    async def get_all_user_events(self, arhpg_id: int, start_date: str):
        events = []
        today_date = datetime.fromisoformat(start_date).date()
        response = await self.get(
            path=f'/api/v1/timetable/user',
            parameters={
                'app_token': API_XLE_TOKEN,
                'context': API_XLE_CONTEXT,
                'date': today_date.strftime('%Y-%m-%d'),
                'unti_ids': arhpg_id
            },
        )
        events.extend(response)
        return events

    async def get_events(self, start_date: str, events_in_request=1):
        events = []
        for days_delta in range(events_in_request):
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

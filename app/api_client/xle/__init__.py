

from app.api_client.api_client_base import ApiClientBase, RequestTypes
from config import API_XLE_CONTEXT, API_XLE_TOKEN


class ApiClientXLE(ApiClientBase):
    async def get_user_events(self, arhpg_id: int, date: str):
        response = await self.get(
            path=f'/api/v1/timetable/user/{arhpg_id}',
            parameters={
                'app_token': API_XLE_TOKEN,
                'context': API_XLE_CONTEXT,
                'date': date
            },
        )
        return response

    async def get_events(self, date: str):
        response = await self.get(
            path=f'/api/v1/timetable/all',
            parameters={
                'app_token': API_XLE_TOKEN,
                'context': API_XLE_CONTEXT,
                'date': date
            },
        )
        return response

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

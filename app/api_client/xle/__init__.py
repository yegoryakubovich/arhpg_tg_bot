

from app.api_client.api_client_base import ApiClientBase, RequestTypes
from config import API_XLE_CONTEXT, API_XLE_TOKEN
from aiohttp import web

class ApiClientXLE(ApiClientBase):
    async def get_user_events(self, arhpg_id: int, date: str, json_response=False):
        response = await self.get(
            path=f'/api/v1/timetable/user/{arhpg_id}',
            parameters={
                'app_token': API_XLE_TOKEN,
                'context': API_XLE_CONTEXT,
                'date': date
            },
            json_response=json_response
        )
        return response

    async def get_events(self, date: str, json_response=False):
        response = await self.get(
            path=f'/api/v1/timetable/all',
            parameters={
                'app_token': API_XLE_TOKEN,
                'context': API_XLE_CONTEXT,
                'date': date
            },
            json_response=json_response
        )
        return response

    async def get(self, path: str, parameters=None, token: str = None, json_response=False):
        if parameters is None:
            parameters = {}
        response = await self.request(
            type=RequestTypes.get,
            path=path,
            token=token,
            parameters=parameters,
        )

        if json_response:
            return web.json_response(response)
        else:
            return response

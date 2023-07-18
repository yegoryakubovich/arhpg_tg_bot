from app.api_client.api_client_base import ApiClientBase
from config import API_XLE_CONTEXT, API_XLE_TOKEN


class ApiClientXLE(ApiClientBase):
    async def get_user_events(self, arhpg_id: int, date: str):
        response = await self.get(
            path=f'/timetable/user/{arhpg_id}',
            parameters={
                'app_token': API_XLE_TOKEN,
                'context': API_XLE_CONTEXT,
                'date': date
            }
        )
        return response

import requests

from app.api_client.api_client_base import ApiClientBase
from config import API_USER_TAG_ID, API_USER_TOKEN, API_USER_HOST


class ApiClientUSER(ApiClientBase):
    @staticmethod
    async def add_tag_user(arhpg_id: int):
        response = requests.post(
            url=f'{API_USER_HOST}/api/v1/users/{arhpg_id}/tags',
            params={'app_token': API_USER_TOKEN},
            json={"tag_id": [API_USER_TAG_ID]},
        )
        return response

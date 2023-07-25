#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from app.api_client.api_client_base import ApiClientBase
from config import API_USER_TAG_ID, API_USER_TOKEN


class ApiClientUSER(ApiClientBase):
    async def add_tag_user(self, arhpg_id: int):
        response = await self.post(
            path=f'/api/v1/users/{arhpg_id}/tags',
            parameters={
                "app_token": API_USER_TOKEN
            },
            data={
                "tag_id": [API_USER_TAG_ID],
                "creator_id": 1,
                "reason": 'a2023_bot'
            },
        )
        print(response)
        return response

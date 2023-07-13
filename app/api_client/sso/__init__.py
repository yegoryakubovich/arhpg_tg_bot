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
from config import API_SSO_CLIENT_ID, API_SSO_REDIRECT_URL, API_SSO_CLIENT_SECRET


class ApiClientSSO(ApiClientBase):
    async def oauth_url_create(self):
        url = await self.url_create(
            path='/oauth2/authorize',
            parameters={
                'client_id': API_SSO_CLIENT_ID,
                'redirect_uri': API_SSO_REDIRECT_URL,
                'response_type': 'code',
            },
        )
        return url

    async def oauth_token_create(self, code):
        response = await self.post(
            path='/oauth2/access_token',
            data={
                'client_id': API_SSO_CLIENT_ID,
                'client_secret': API_SSO_CLIENT_SECRET,
                'grant_type': 'authorization_code',
                'redirect_uri': '',
                'code': code,
            },
        )
        token = response['access_token']
        return token

    async def user_get(self, token: str):
        response = await self.get(
            path='/users/me',
            token=token,
        )
        return response

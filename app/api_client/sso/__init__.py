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

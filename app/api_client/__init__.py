 
from app.api_client.event import ApiClientEVENT
from app.api_client.sso import ApiClientSSO
from app.api_client.user import ApiClientUSER
from app.api_client.xle import ApiClientXLE
from config import API_SSO_HOST, API_XLE_HOST, API_USER_HOST, API_EVENT_HOST


class ApiClient:
    sso = ApiClientSSO(host=API_SSO_HOST)
    xle = ApiClientXLE(host=API_XLE_HOST)
    user = ApiClientUSER(host=API_USER_HOST)
    event = ApiClientEVENT(host=API_EVENT_HOST)

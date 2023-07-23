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


from configparser import ConfigParser


config = ConfigParser()
config.read('config.ini')

config_db = config['db']
config_api = config['api']
config_tg = config['tg']
config_url = config['test_url']
config_usedesk = config['usedesk']

MYSQL_HOST = config_db['host']
MYSQL_PORT = int(config_db['port'])
MYSQL_USER = config_db['user']
MYSQL_PASSWORD = config_db['password']
MYSQL_NAME = config_db['name']

API_SSO_HOST = config_api['sso_host']
API_SSO_CLIENT_ID = config_api['sso_client_id']
API_SSO_CLIENT_SECRET = config_api['sso_client_secret']
API_SSO_REDIRECT_URL = config_api['sso_redirect_url']

API_XLE_HOST = config_api['xle_host']
API_XLE_CONTEXT = config_api['xle_context']
API_XLE_TOKEN = config_api['xle_token']

TG_BOT_USERNAME = config_tg['bot_username']
TG_BOT_TOKEN = config_tg['bot_token']

URL_ALL_PROGRAMS = config_url['all_programs']
URL_MY_PROGRAMS = config_url['my_programs']
URL_PROGRAM = config_url['program']

USEDESK_HOST = config_usedesk['usedesk_host']
USEDESK_ID = config_usedesk['usedesk_id']
USEDESK_API_TOKEN = config_usedesk['usedesk_token']

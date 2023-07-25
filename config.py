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
config_url = config['urls']
config_usedesk = config['usedesk']
config_kafka = config['kafka']
config_vpn = config['vpn']


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

API_USER_HOST = config_api['user_host']
API_USER_TOKEN = config_api['user_token']
API_USER_TAG_ID = config_api['user_tag_id']

TG_BOT_USERNAME = config_tg['bot_username']
TG_BOT_TOKEN = config_tg['bot_token']

URL_ALL_PROGRAM = config_url['all_program']
URL_MY_PROGRAMS = config_url['my_programs']
URL_PROGRAM = config_url['program']

USEDESK_HOST = config_usedesk['usedesk_host']
USEDESK_ID = config_usedesk['usedesk_id']
USEDESK_API_TOKEN = config_usedesk['usedesk_token']

KAFKA_BOOTSTRAP_SERVERS = config_kafka['kafka_bootstrap_servers']
KAFKA_SECURITY_PROTOCOL = config_kafka['kafka_security_protocol']
KAFKA_SASL_MECHANISM = config_kafka['kafka_sasl_mechanism']
KAFKA_SASL_PLAIN_USERNAME = config_kafka['kafka_sasl_plain_username']
KAFKA_SASL_PLAIN_PASSWORD = config_kafka['kafka_sasl_plain_password']

VPN_HOST = config_vpn['vpn_host']
VPN_USERNAME = config_vpn['vpn_username']
VPN_PASSWORD = config_vpn['vpn_password']

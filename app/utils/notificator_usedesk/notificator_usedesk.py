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


from requests import get

from app.db.manager import db_manager
from app.repositories import Ticket
from config import USEDESK_HOST, USEDESK_API_TOKEN


@db_manager
async def notificator_usedesk():
    for ticket in Ticket.list_waiting_get():
        response = get(
            url=f'{USEDESK_HOST}/ticket',
            params={
                'api_token': USEDESK_API_TOKEN,
                'ticket_id': ticket.ticket_id,
            },
        )
        if response.status_code == 200:
            response = response.json()
            print(response)
            '''if status != ticket.status:
                ticket.status = status
                ticket.save()
                print(response['last_message']['message'])'''

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


import asyncio
import re

import aiohttp
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bs4 import BeautifulSoup
from requests import get

from app.aiogram.bot import bot_get
from app.db.manager import db_manager
from app.repositories import Ticket, Text
from app.repositories.ticket import TicketStates
from config import USEDESK_HOST, USEDESK_API_TOKEN


lock = asyncio.Lock()


@db_manager
async def notificator_usedesk():
    bot = bot_get()
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
            ticket_status = response['ticket']['status_id']
            ticket_response = response['comments'][0]['message']

            if ticket_status == 2:
                if ticket_response:
                    bs = BeautifulSoup(ticket_response, features='html.parser')
                    response_text = bs.get_text()
                else:
                    response_text = await Ticket.update_state(ticket.ticket_id, TicketStates.error)

                if '<img' in ticket_response.lower():
                    async with aiohttp.ClientSession() as session:
                        image_url = re.findall(r'<img.+?src="(.+?)"', ticket_response)[0]
                        async with session.get(image_url) as resp:
                            if resp.status == 200:
                                image_bytes = await resp.read()

                    keyboard = InlineKeyboardMarkup().add(
                        InlineKeyboardButton(text=Text.get('menu_support'), callback_data='support_usedesk')
                    )

                    await Ticket.update_state(ticket.ticket_id, TicketStates.completed)

                    await bot.send_photo(
                        chat_id=ticket.user.tg_user_id,
                        photo=image_bytes,
                        caption=response_text,
                        parse_mode='html',
                        reply_markup=keyboard,
                    )
                else:
                    keyboard = InlineKeyboardMarkup().add(
                        InlineKeyboardButton(text=Text.get('menu_support'), callback_data='support_usedesk')
                    )

                    await Ticket.update_state(ticket.ticket_id, TicketStates.completed)

                    await bot.send_message(
                        chat_id=ticket.user.tg_user_id,
                        text=response_text,
                        parse_mode='html',
                        reply_markup=keyboard,
                    )

            elif ticket_status == 4:
                await Ticket.update_state(ticket.ticket_id, TicketStates.error)

    await bot.close()

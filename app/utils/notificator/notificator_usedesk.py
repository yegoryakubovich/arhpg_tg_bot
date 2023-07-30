import asyncio
import os
import re
import tempfile

import aiohttp
from aiogram import types
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
            file_url_list = response['comments'][0]['files']
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
                elif file_url_list and isinstance(file_url_list, list) and len(file_url_list) > 0:
                    doc_url = file_url_list[0]['file']
                    async with aiohttp.ClientSession() as session:
                        async with session.get(doc_url) as resp:
                            if resp.status == 200:
                                doc_bytes = await resp.read()

                    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
                        tmp_file.write(doc_bytes)
                        tmp_filename = tmp_file.name

                    keyboard = InlineKeyboardMarkup().add(
                        InlineKeyboardButton(text=Text.get('menu_support'), callback_data='support_usedesk')
                    )

                    await Ticket.update_state(ticket.ticket_id, TicketStates.completed)

                    with open(tmp_filename, 'rb'):
                        await bot.send_document(
                            chat_id=ticket.user.tg_user_id,
                            document=types.input_file.InputFile(tmp_filename),
                            caption=response_text,
                            parse_mode='html',
                            reply_markup=keyboard,
                        )

                    os.remove(tmp_filename)
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

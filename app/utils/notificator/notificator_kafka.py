#
# (c) 2023, Yegor Yakubovich
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


import json

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from confluent_kafka import Consumer

from app.aiogram import bot_get
from app.db.manager import db_manager
from app.repositories import User, Text
from app.utils.api_client import api_client
from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_SASL_MECHANISM, KAFKA_SASL_PLAIN_USERNAME, KAFKA_SECURITY_PROTOCOL, \
    KAFKA_SASL_PLAIN_PASSWORD, URL_PROGRAM


@db_manager
async def notificator_kafka():
    bot = bot_get()
    kafka_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'security.protocol': KAFKA_SECURITY_PROTOCOL,
        'sasl.mechanism': KAFKA_SASL_MECHANISM,
        'sasl.username': KAFKA_SASL_PLAIN_USERNAME,
        'sasl.password': KAFKA_SASL_PLAIN_PASSWORD,
        'group.id': 'user_consumer_group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(kafka_config)

    topic = 'timetable'

    consumer.subscribe([topic])

    while True:
        msg = consumer.poll(10)

        if msg is None:
            continue
        else:
            value = msg.value()
            if value is not None:
                value = value.decode('utf-8')
                data = json.loads(value)
                message_type = data.get('type')
                if message_type == 'event':
                    message_action = data.get('action')
                    if message_action == 'update':
                        event_id = data.get('id', {}).get('event', {}).get('uuid')
                        type_id = data.get('type_ids', {}).get('uuid')
                        arhpg_ids = await User.get_all_arhpg_id()
                        user_data = await api_client.xle.get_events_user(type_id, arhpg_ids)
                        participants = [user for user in user_data if user.get('participant', True)]
                        tg_user_ids = []
                        for participant in participants:
                            arhpg_id = participant.get('unti_id')
                            tg_user_id = await User.get_tg_user_id(arhpg_id)
                            if tg_user_id is not None:
                                tg_user_ids.append(tg_user_id)
                        if tg_user_ids:
                            update_program = Text.get('update_program')
                            event_text = Text.get('program')
                            event_url = f"{URL_PROGRAM}{event_id}"
                            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(event_text, url=event_url)]])
                            for tg_user_id in tg_user_ids:
                                bot.send_message(chat_id=tg_user_id, text=update_program, reply_markup=keyboard)

    consumer.close()

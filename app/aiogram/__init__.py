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


from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType
from aiogram.utils import executor

from app.aiogram.handlers.faqs import handler_faqs
from app.aiogram.handlers.menu import handler_menu
from app.aiogram.handlers.program import handler_program
from app.aiogram.handlers.start import handler_start
from app.aiogram.handlers.support import handler_support
from app.aiogram.states import States
from config import TG_BOT_TOKEN


bot = Bot(
    token=TG_BOT_TOKEN,
)
# storage = RedisStorage2(
#     host=REDIS_HOST,
#     port=REDIS_PORT,
#     password=REDIS_PASSWORD,
#     db=REDIS_DB,
#     pool_size=10,
#     prefix=REDIS_PREFIX,
# )
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
HANDLERS = [
    {'handler': handler_start, 'state': '*', 'content_types': [ContentType.TEXT], 'commands': ['start', 'menu']},
    {'handler': handler_menu, 'state': States.menu, 'content_types': [ContentType.TEXT]},
    {'handler': handler_program, 'state': States.program, 'content_types': [ContentType.TEXT]},
    {'handler': handler_faqs, 'state': States.faqs, 'content_types': [ContentType.TEXT]},
    {'handler': handler_support, 'state': States.support, 'content_types': [ContentType.TEXT]},
]


def handlers_create():
    [
        dp.register_message_handler(
            callback=h.get('handler'),
            state=h.get('state'),
            content_types=h.get('content_types'),
            commands=h.get('commands'),
        )
        for h in HANDLERS
    ]


def bot_create():
    handlers_create()
    executor.start_polling(dp)

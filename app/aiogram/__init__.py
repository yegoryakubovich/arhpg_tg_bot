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
from aiogram.utils import executor

from app.aiogram.handlers.register import handlers_register
from config import TG_BOT_TOKEN


bot = Bot(
    token=TG_BOT_TOKEN,
)
storage = MemoryStorage()
#  RedisStorage2(
#     host=REDIS_HOST,
#     port=REDIS_PORT,
#     password=REDIS_PASSWORD,
#     db=REDIS_DB,
#     pool_size=10,
#     prefix=REDIS_PREFIX,
# )
dp = Dispatcher(bot=bot, storage=storage)


def bot_create():
    handlers_register(dp=dp)
    executor.start_polling(dispatcher=dp)

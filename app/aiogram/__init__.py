from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from app.aiogram.bot import bot_get
from app.aiogram.handlers.register import handlers_register

storage = MemoryStorage()
#  RedisStorage2(
#     host=REDIS_HOST,
#     port=REDIS_PORT,
#     password=REDIS_PASSWORD,
#     db=REDIS_DB,
#     pool_size=10,
#     prefix=REDIS_PREFIX,
# )
dp = Dispatcher(bot=bot_get(), storage=storage)


def bot_create():
    handlers_register(dp=dp)
    executor.start_polling(dispatcher=dp, )

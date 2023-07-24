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


from app.aiogram import bot_create, dp

from app.db import tables_create
from app.utils.notificator import notificator_create
from app.utils.notificator_kafka import notificator_kafka_create
from app.utils.notificaror_program import notificator_program_create
from app.utils.notificator_usedesk import notificator_usedesk_create


def app_create():
    tables_create()
    notificator_usedesk_create()
    notificator_create()
    notificator_kafka_create()
    notificator_program_create()
    bot_create()

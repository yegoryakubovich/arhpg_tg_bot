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


from aiogram import Dispatcher


from app.aiogram.handlers import handlers, handlers_inline


def handlers_register(dp: Dispatcher):
    [
        dp.register_message_handler(
            callback=h.get('handler'),
            state=h.get('state'),
            content_types=h.get('content_types'),
            commands=h.get('commands'),
        )
        for h in handlers
    ]

    [
        dp.register_callback_query_handler(
            h.get('handler'),
            lambda callback_query, prefix=h.get('prefix'): callback_query.data.startswith(prefix),
            state=h.get('state')
        )
        for h in handlers_inline
    ]

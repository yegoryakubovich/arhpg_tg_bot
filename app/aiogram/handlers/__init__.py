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


from aiogram.types import ContentType

from app.aiogram.handlers.menu import handler_menu
from app.aiogram.handlers.program import handler_program
from app.aiogram.handlers.start import handler_start
from app.aiogram.handlers.faqs.button import handler_faqs_button
from app.aiogram.handlers.faqs.faqs import handler_faqs
from app.aiogram.handlers.support import handler_support
from app.aiogram.states import States


handlers = (
    {'handler': handler_start, 'state': '*', 'content_types': [ContentType.TEXT], 'commands': ['start', 'menu']},
    {'handler': handler_menu, 'state': States.menu, 'content_types': [ContentType.TEXT]},
    {'handler': handler_program, 'state': States.program, 'content_types': [ContentType.TEXT]},
    {'handler': handler_faqs, 'state': States.faqs, 'content_types': [ContentType.TEXT]},
    {'handler': handler_support, 'state': States.support, 'content_types': [ContentType.TEXT]},
)
handlers_inline = (
    {'handler': handler_faqs_button, 'state': '*'},
)
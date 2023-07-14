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
from enum import Enum

from app.repositories.base import BaseRepository
from app.db.models import FaqModel


class FaqTypes:
    url = 'url'
    text = 'text'


class FaqAttachmentTypes(Enum):
    url = 'url'
    text = 'text'
    image = 'image'
    file = 'file'


class Faq(BaseRepository):
    @staticmethod
    def list_get() -> list[FaqModel]:
        faqs = FaqModel.select().order_by(FaqModel.priority.asc())
        return faqs

    @staticmethod
    def get(id: int) -> FaqModel:
        faq = FaqModel.get(FaqModel.id == id)
        return faq

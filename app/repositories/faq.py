 
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

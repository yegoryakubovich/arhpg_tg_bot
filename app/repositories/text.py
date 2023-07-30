from app.repositories.base import BaseRepository
from app.db.models import TextModel


class Text(BaseRepository):
    @staticmethod
    def get(key: str) -> str:
        text = TextModel.get_or_none(TextModel.key == key)
        if not text:
            return '404'
        return text.value

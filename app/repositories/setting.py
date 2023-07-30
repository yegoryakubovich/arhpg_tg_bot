from app.repositories.base import BaseRepository
from app.db.models import SettingModel


class Setting(BaseRepository):
    @staticmethod
    async def events_count() -> int:
        setting = SettingModel.get(SettingModel.key == 'events_count')
        return int(setting.value)

    @staticmethod
    async def events_in_request() -> int:
        setting = SettingModel.get(SettingModel.key == 'events_in_request')
        return int(setting.value)

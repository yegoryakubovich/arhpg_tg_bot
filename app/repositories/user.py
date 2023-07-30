from app.db.models import UserModel
from app.repositories.base import BaseRepository
from app.utils.api_client import api_client


class User(BaseRepository):
    @staticmethod
    async def create(
            arhpg_id: int,
            arhpg_token: str,
            tg_user_id: int,
            firstname: str,
            lastname: str,
            email: str,
    ) -> UserModel:
        user = UserModel.get_or_none(UserModel.tg_user_id == tg_user_id)
        if not user:
            user = UserModel(
                arhpg_id=arhpg_id,
                arhpg_token=arhpg_token,
                tg_user_id=tg_user_id,
                firstname=firstname,
                lastname=lastname,
                email=email,
            )
            user.save()
            return user

        user.arhpg_token = arhpg_token
        user.save()

        return user

    @staticmethod
    async def is_authorized(tg_user_id: int) -> bool:
        user = UserModel.get_or_none(UserModel.tg_user_id == tg_user_id)

        if user:
            if user.arhpg_token:
                sso_user = await api_client.sso.user_get(token=user.arhpg_token)
                arhpg_id = sso_user.get('leader_id')
                if not arhpg_id:
                    user.arhpg_token = False
                    user.save()
                    return False
                return True
        return False

    @staticmethod
    async def get(tg_user_id: int) -> UserModel:
        user = UserModel.get(UserModel.tg_user_id == tg_user_id)
        return user

    @staticmethod
    async def get_all_arhpg_id() -> list:
        all_users = UserModel.select()
        all_arhpg_id = [user.arhpg_id for user in all_users]
        return all_arhpg_id

    @staticmethod
    async def get_tg_user_id(arhpg_id: int) -> int:
        user = UserModel.get(UserModel.arhpg_id == arhpg_id)
        tg_user_id = user.tg_user_id
        return tg_user_id

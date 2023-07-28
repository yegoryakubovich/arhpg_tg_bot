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


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


class User(BaseRepository):
    model = UserModel

    def create(self, arhpg_id: int, arhpg_token: str, tg_user_id: int, firstname: str, lastname: str):
        user = self.model(
            arhpg_id=arhpg_id,
            arhpg_token=arhpg_token,
            tg_user_id=tg_user_id,
            firstname=firstname,
            lastname=lastname,
        )
        user.save()
        return user

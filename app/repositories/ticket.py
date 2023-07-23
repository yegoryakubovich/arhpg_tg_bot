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


from app.repositories.base import BaseRepository
from app.db.models import TicketModel, UserModel


class TicketStates:
    waiting = 'waiting'
    completed = 'completed'
    error = 'error'


class Ticket(BaseRepository):
    @staticmethod
    def list_waiting_get() -> list[TicketModel]:
        tickets = TicketModel.select().where(TicketModel.state == TicketStates.waiting).execute()
        return tickets

    @staticmethod
    async def create(
            user: UserModel,
            message: str,
            state: str = TicketStates.waiting,
            ticket_id: int = None,
    ) -> TicketModel:
        ticket = TicketModel(
            user=user,
            message=message,
            state=state,
            ticket_id=ticket_id,
        )
        ticket.save()
        return ticket

    @staticmethod
    async def update_state(ticket_id: int, new_state: str):
        ticket = TicketModel.get_or_none(TicketModel.ticket_id == ticket_id)
        if ticket:
            ticket.state = new_state
            ticket.save()





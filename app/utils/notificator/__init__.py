#
# (c) 2023, Yegor Yakubovich
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


from asyncio import new_event_loop, set_event_loop

from time import sleep
from threading import Thread
import aioschedule as schedule

from app.utils.notificator.notificator import notificator
# from app.utils.notificator.notificator_kafka import notificator_kafka
from app.utils.notificator.notificator_usedesk import notificator_usedesk


def notificator_thread():
    loop = new_event_loop()
    set_event_loop(loop)

    schedule.every(10).seconds.do(notificator)
    # schedule.every(10).seconds.do(notificator_kafka)
    schedule.every(1).minute.do(notificator_usedesk)
    while True:
        loop.run_until_complete(schedule.run_pending())
        sleep(10)


def notificator_create():
    thread = Thread(target=notificator_thread, args=())
    thread.start()

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


from datetime import datetime

from app.aiogram import bot_get
from app.db.manager import db_manager
from app.db.models.notification_report import NotificationReport
from app.db.models.notification_user import NotificationUser
from app.db.models.user import User
from app.repositories.notification import Notification

bot = bot_get()


@db_manager
async def notificator():
    current_datetime = datetime.now()
    notifications = Notification.list_waiting_get(current_datetime)
    for notification in notifications:
        await send_notification(notification)


@db_manager
async def send_notification(notification):
    users = [user for user in User.select().join(NotificationUser).where(NotificationUser.notification == notification)]
    for user in users:
        report = NotificationReport(
            notification=notification,
            user=user,
            state='waiting',
            datetime=notification.datetime,
        )
        await bot.send_message(user.tg_user_id, notification.text)
        notification.state = 'completed'
        notification.save()
        report.state = 'completed'
        report.save()


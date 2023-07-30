from app.db.models.setting import Setting as SettingModel
from app.db.models.category_text import CategoryText as CategoryTextModel
from app.db.models.faq import Faq as FaqModel
from app.db.models.faq_attachment import FaqAttachment as FaqAttachmentModel
from app.db.models.text import Text as TextModel
from app.db.models.ticket import Ticket as TicketModel
from app.db.models.user import User as UserModel
from app.db.models.notification import Notification as NotificationModel
from app.db.models.notification_user import NotificationUser as NotificationUserModel
from app.db.models.notification_report import NotificationReport as NotificationReportModel
from app.db.models.users_tags import UserTag

models = (
    SettingModel,
    CategoryTextModel,
    TextModel,
    UserModel,
    FaqModel,
    FaqAttachmentModel,
    TicketModel,
    NotificationModel,
    NotificationUserModel,
    NotificationReportModel,
    UserTag,
)

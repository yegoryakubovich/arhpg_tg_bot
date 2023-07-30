from aiogram import types

from app.db.manager import db_manager
from app.db.models.faq_attachment import FaqAttachment
from app.repositories import FaqAttachmentTypes, Faq
from app.utils.decorators import user_get


@db_manager
@user_get
async def handler_faqs_button(callback_query: types.CallbackQuery, user):
    data = callback_query.data.split('_')
    if len(data) == 2 and data[0] == 'faqs':
        faq_id = int(data[1])
        faqs = Faq.list_get()
        faq = next((faq for faq in faqs if faq.id == faq_id), None)
        if faq and faq.type == FaqAttachmentTypes.text.value:
            text_attachments = FaqAttachment.select().where(
                FaqAttachment.faq == faq,
                FaqAttachment.type == FaqAttachmentTypes.text.value
            )
            image_attachments = FaqAttachment.select().where(
                FaqAttachment.faq == faq,
                FaqAttachment.type == FaqAttachmentTypes.image.value
            )
            file_attachments = FaqAttachment.select().where(
                FaqAttachment.faq == faq,
                FaqAttachment.type == FaqAttachmentTypes.file.value
            )

            caption = '\n'.join(a.value for a in text_attachments)

            if image_attachments and text_attachments and file_attachments:
                photos = []
                for image_attachment in image_attachments:
                    photos.append(types.InputMediaPhoto(
                        media=image_attachment.value,
                        caption=caption if image_attachment == image_attachments[0] else None,
                        parse_mode='html'
                    ))

                documents = []
                for file_attachment in file_attachments:
                    documents.append(types.InputMediaDocument(
                        media=file_attachment.value,
                        parse_mode='html'
                    ))

                if photos:
                    await callback_query.message.reply_media_group(media=photos)

                if documents:
                    await callback_query.message.answer_media_group(media=documents)
            else:
                media = []

                if image_attachments:
                    for image_attachment in image_attachments:
                        media.append(types.InputMediaPhoto(
                            media=image_attachment.value,
                            caption=caption if image_attachment == image_attachments[0] else None,
                            parse_mode='html'
                        ))

                if file_attachments:
                    for file_attachment in file_attachments:
                        media.append(types.InputMediaDocument(
                            media=file_attachment.value,
                            caption=caption if file_attachment == file_attachments[-1] else None,
                            parse_mode='html'
                        ))

                if media:
                    await callback_query.message.reply_media_group(media=media)
                else:
                    await callback_query.message.reply(
                        text=caption,
                        parse_mode='html')

                await callback_query.answer()

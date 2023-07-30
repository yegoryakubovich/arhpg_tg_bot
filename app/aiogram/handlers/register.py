from aiogram import Dispatcher

from app.aiogram.handlers import handlers, handlers_inline


def handlers_register(dp: Dispatcher):
    [
        dp.register_message_handler(
            callback=h.get('handler'),
            state=h.get('state'),
            content_types=h.get('content_types'),
            commands=h.get('commands'),
        )
        for h in handlers
    ]

    [
        dp.register_callback_query_handler(
            h.get('handler'),
            lambda callback_query, prefix=h.get('prefix'): callback_query.data.startswith(prefix),
            state=h.get('state')
        )
        for h in handlers_inline
    ]

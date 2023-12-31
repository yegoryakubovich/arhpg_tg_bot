from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from app.repositories import User, Text
from app.utils.api_client import api_client

not_returned = False


def user_get(function):
    async def wrapper(*args):
        obj = args[0]
        tg_user_id = obj.from_user.id

        if type(obj) is Message:
            message = obj
            if hasattr(message, 'photo'):
                pass
            if hasattr(message, 'text') and message.text:
                commands = message.text.split()

                if len(commands) == 2:
                    arhpg_token = commands[-1]

                    sso_user = await api_client.sso.user_get(token=arhpg_token)
                    arhpg_id = sso_user.get('unti_id')
                    firstname = sso_user.get('firstname')
                    lastname = sso_user.get('lastname')
                    email = sso_user.get('email')

                    if arhpg_id:
                        await User.create(
                            arhpg_id=arhpg_id,
                            arhpg_token=arhpg_token,
                            tg_user_id=tg_user_id,
                            firstname=firstname,
                            lastname=lastname,
                            email=email,
                        )
                        await api_client.user.add_tag_user(arhpg_id)

        is_authorized = await User.is_authorized(tg_user_id=tg_user_id)
        if not is_authorized:
            url = await api_client.sso.oauth_url_create()

            kb = InlineKeyboardMarkup(row_width=1)
            kb.add(InlineKeyboardButton(
                text=Text.get('greetings_sso_button'),
                url=url,
            ))
            await obj.answer(text=Text.get('greetings'))
            await obj.answer(text=Text.get('greetings_sso'), reply_markup=kb)
            return

        user = await User.get(tg_user_id=tg_user_id)

        kwargs = {}

        if type(obj) is Message:
            kwargs['message'] = obj
        elif type(obj) is CallbackQuery:
            kwargs['callback_query'] = obj

        if not not_returned:
            kwargs['user'] = user

        return await function(**kwargs)

    return wrapper

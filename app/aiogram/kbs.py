from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.repositories import Text


class Kbs:
    @staticmethod
    async def back():
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton(text=Text.get('back')))
        return kb

    @staticmethod
    async def menu():
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton(text=Text.get('menu_program')))
        kb.add(KeyboardButton(text=Text.get('menu_faqs')))
        kb.add(KeyboardButton(text=Text.get('menu_support')))
        return kb

    @staticmethod
    async def programs():
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton(text=Text.get('user_programs')))
        kb.add(KeyboardButton(text=Text.get('general_programs')))
        kb.add(KeyboardButton(text=Text.get('back')))
        return kb

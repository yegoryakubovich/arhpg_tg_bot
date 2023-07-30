from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    menu = State()
    programs = State()
    support = State()

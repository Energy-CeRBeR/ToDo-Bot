from aiogram.fsm.state import StatesGroup, State


class AuthorizeState(StatesGroup):
    get_email = State()
    get_password = State()

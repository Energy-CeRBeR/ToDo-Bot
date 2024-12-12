from aiogram.fsm.state import StatesGroup, State


class CategoryState(StatesGroup):
    get_name = State()
    get_color = State()
    get_new_name = State()

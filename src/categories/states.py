from aiogram.fsm.state import StatesGroup, State


class CreateCategoryState(StatesGroup):
    get_name = State()
    get_color = State()

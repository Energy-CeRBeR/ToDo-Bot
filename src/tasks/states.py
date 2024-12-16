from aiogram.fsm.state import StatesGroup, State


class TaskState(StatesGroup):
    get_category = State()
    get_name = State()
    get_description = State()
    get_priority = State()
    get_date = State()
    get_year = State()
    get_month = State()

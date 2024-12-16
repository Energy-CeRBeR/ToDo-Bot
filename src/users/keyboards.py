from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.users.lexicon import LEXICON as USER_LEXICON


def profile_keyboard() -> InlineKeyboardMarkup:
    categories_button = InlineKeyboardButton(
        text=USER_LEXICON["categories_button_text"],
        callback_data="show_categories"
    )
    tasks_button = InlineKeyboardButton(
        text=USER_LEXICON["tasks_button_text"],
        callback_data="tasks_menu"
    )

    return InlineKeyboardMarkup(inline_keyboard=[[categories_button], [tasks_button]])


def yes_no_keyboard(callback_data: str) -> InlineKeyboardMarkup:
    yes_button = InlineKeyboardButton(text="Да", callback_data="yes_" + callback_data)
    no_button = InlineKeyboardButton(text="Нет", callback_data="no_" + callback_data)

    return InlineKeyboardMarkup(inline_keyboard=[[yes_button], [no_button]])

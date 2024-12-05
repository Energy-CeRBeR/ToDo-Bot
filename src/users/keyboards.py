from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.users.lexicon import LEXICON as USER_LEXICON


def profile_keyboard() -> InlineKeyboardMarkup:
    categories_button = InlineKeyboardButton(
        text=USER_LEXICON["categories_button_text"],
        callback_data="show_categories"
    )
    tasks_button = InlineKeyboardButton(
        text=USER_LEXICON["tasks_button_text"],
        callback_data="show_tasks"
    )

    return InlineKeyboardMarkup(inline_keyboard=[[categories_button], [tasks_button]])

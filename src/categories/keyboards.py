from typing import List, Dict

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .lexicon import LEXICON as CATEGORIES_LEXICON
from utils.universal_lexicon import LEXICON as UNIVERSAL_LEXICON


def all_categories_keyboard(categories: List[Dict]) -> InlineKeyboardMarkup:
    buttons = list()
    for category in categories:
        cur_category = InlineKeyboardButton(
            text=category['name'],
            callback_data=f"get_category_{category['id']}"
        )
        buttons.append([cur_category])

    exit_button = InlineKeyboardButton(
        text=UNIVERSAL_LEXICON["exit"],
        callback_data="exit"
    )
    back_page_button = InlineKeyboardButton(
        text=UNIVERSAL_LEXICON["back_page"],
        callback_data="back_cat_page"
    )
    next_page_button = InlineKeyboardButton(
        text=UNIVERSAL_LEXICON["next_page"],
        callback_data="next_cat_page"
    )

    return InlineKeyboardMarkup(inline_keyboard=[*buttons, [back_page_button, exit_button, next_page_button]])


def show_category_keyboard(category: Dict):
    pass

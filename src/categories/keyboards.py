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


def all_categories_keyboard_for_tasks(categories: List[Dict]) -> InlineKeyboardMarkup:
    buttons = list()
    for category in categories:
        cur_category = InlineKeyboardButton(
            text=category['name'],
            callback_data=f"get_category_{category['id']}"
        )
        buttons.append([cur_category])

    back_page_button = InlineKeyboardButton(
        text=UNIVERSAL_LEXICON["back_page"],
        callback_data="back_cat_page"
    )
    next_page_button = InlineKeyboardButton(
        text=UNIVERSAL_LEXICON["next_page"],
        callback_data="next_cat_page"
    )

    return InlineKeyboardMarkup(inline_keyboard=[*buttons, [back_page_button, next_page_button]])


def category_about_keyboard(category_id: int) -> InlineKeyboardMarkup:
    edit_name_button = InlineKeyboardButton(
        text=CATEGORIES_LEXICON["edit_name"],
        callback_data=f"edit_category_name_{category_id}"
    )
    category_tasks_button = InlineKeyboardButton(
        text=CATEGORIES_LEXICON["show_category_tasks"],
        callback_data=f"show_category_tasks_{category_id}"
    )
    delete_category_button = InlineKeyboardButton(
        text=CATEGORIES_LEXICON["delete_category"],
        callback_data=f"delete_category_{category_id}"
    )
    back_to_categories_button = InlineKeyboardButton(
        text=CATEGORIES_LEXICON["back_to_categories"],
        callback_data="back_to_categories"
    )
    exit_button = InlineKeyboardButton(
        text=UNIVERSAL_LEXICON["exit"],
        callback_data="exit"
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [edit_name_button],
            [category_tasks_button],
            [back_to_categories_button],
            [delete_category_button],
            [exit_button]
        ]
    )


def yes_no_keyboard() -> InlineKeyboardMarkup:
    yes_button = InlineKeyboardButton(
        text=UNIVERSAL_LEXICON["yes_button"],
        callback_data="yes"
    )
    no_button = InlineKeyboardButton(
        text=UNIVERSAL_LEXICON["no_button"],
        callback_data="no"
    )

    return InlineKeyboardMarkup(inline_keyboard=[[yes_button], [no_button]])

import datetime
from typing import List, Dict

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .lexicon import LEXICON as TASKS_LEXICON
from utils.universal_lexicon import LEXICON as UNIVERSAL_LEXICON
from utils.utils import get_month_by_number, get_day_by_number, get_month_data


def show_tasks_keyboard(tasks: List[Dict]) -> InlineKeyboardMarkup:
    buttons = list()
    for task in tasks:
        cur_task = InlineKeyboardButton(
            text=f"{task['name']} ({task['date']})",
            callback_data=f"get_task_{task['id']}"
        )
        buttons.append([cur_task])

    exit_button = InlineKeyboardButton(
        text=UNIVERSAL_LEXICON["exit"],
        callback_data="exit"
    )
    prev_page_button = InlineKeyboardButton(
        text=UNIVERSAL_LEXICON["back_page"],
        callback_data="prev_task_page"
    )
    next_page_button = InlineKeyboardButton(
        text=UNIVERSAL_LEXICON["next_page"],
        callback_data="next_task_page"
    )

    return InlineKeyboardMarkup(inline_keyboard=[*buttons, [prev_page_button, exit_button, next_page_button]])


def task_about_keyboard(task_id: int, task_status: bool) -> InlineKeyboardMarkup:
    edit_task_button = InlineKeyboardButton(
        text=TASKS_LEXICON["edit_task"],
        callback_data=f"edit_task_menu_{task_id}"
    )
    edit_status_button = InlineKeyboardButton(
        text=TASKS_LEXICON["edit_status"][int(task_status)],
        callback_data=f"edit_task_status_{task_id}"
    )
    delete_button = InlineKeyboardButton(
        text=TASKS_LEXICON["delete_task"],
        callback_data=f"delete_task_{task_id}"
    )
    exit_button = InlineKeyboardButton(
        text=UNIVERSAL_LEXICON["exit"],
        callback_data="exit"
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[[edit_task_button], [edit_status_button], [delete_button], [exit_button]]
    )


def add_description_keyboard() -> InlineKeyboardMarkup:
    no_add_button = InlineKeyboardButton(
        text=TASKS_LEXICON["no_add_description"],
        callback_data="no_add_description"
    )

    return InlineKeyboardMarkup(inline_keyboard=[[no_add_button]])


def select_priority_keyboard() -> InlineKeyboardMarkup:
    low_priority_button = InlineKeyboardButton(
        text=TASKS_LEXICON["low_priority"],
        callback_data="low_priority"
    )
    medium_priority_button = InlineKeyboardButton(
        text=TASKS_LEXICON["medium_priority"],
        callback_data="medium_priority"
    )
    high_priority_button = InlineKeyboardButton(
        text=TASKS_LEXICON["high_priority"],
        callback_data="high_priority"
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[[low_priority_button], [medium_priority_button], [high_priority_button]]
    )


def tasks_calendar_keyboard(date=datetime.date.today()) -> InlineKeyboardMarkup:
    year, month, day = date.year, date.month, date.day

    prev_year_button = InlineKeyboardButton(
        text=TASKS_LEXICON["prev_calendar_page"],
        callback_data=f"calendar_page_{year - 1}-{month}"
    )
    cur_year_button = InlineKeyboardButton(
        text=str(year),
        callback_data=f"calendar_select_year_{month}"
    )
    next_year_button = InlineKeyboardButton(
        text=TASKS_LEXICON["next_calendar_page"],
        callback_data=f"calendar_page_{year + 1}-{month}"
    )

    prev_month_button = InlineKeyboardButton(
        text=TASKS_LEXICON["prev_calendar_page"],
        callback_data=f"calendar_page_{year}-{(month - 1) % 12 if month != 1 else 12}"
    )
    cur_month_button = InlineKeyboardButton(
        text=get_month_by_number(month),
        callback_data=f"calendar_select_month_{year}"
    )
    next_month_button = InlineKeyboardButton(
        text=TASKS_LEXICON["next_calendar_page"],
        callback_data=f"calendar_page_{year}-{(month + 1) % 13 if month != 12 else 1}"
    )

    start_month, days = get_month_data(year, month)
    end_month = start_month + days

    lines = end_month // 7 + (end_month % 7 != 0)
    calendar_buttons = list(list() for _ in range(lines))
    ind = 0
    count = 1

    header_line = list(
        InlineKeyboardButton(text=get_day_by_number(day_num)[:3], callback_data=" ") for day_num in range(7)
    )

    while ind != lines:
        while count <= start_month:
            calendar_buttons[ind].append(InlineKeyboardButton(text=" ", callback_data=" "))
            count += 1

        while len(calendar_buttons[ind]) < 7:
            if count <= end_month:
                calendar_buttons[ind].append(InlineKeyboardButton(
                    text=str(count - start_month),
                    callback_data=f"calendar_get_{year}-{month}-{count - start_month}")
                )
            else:
                calendar_buttons[ind].append(InlineKeyboardButton(text=" ", callback_data=" "))
            count += 1

        ind += 1

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [prev_year_button, cur_year_button, next_year_button],
            [prev_month_button, cur_month_button, next_month_button],
            [*header_line],
            *calendar_buttons
        ]
    )


def select_month_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text=get_month_by_number(month),
            callback_data=f"get_month_{month}"
        ) for month in range(1, 13)
    ]

    return InlineKeyboardMarkup(inline_keyboard=[buttons[:3], buttons[3:6], buttons[6:9], buttons[9:12]])


def tasks_menu_keyboard() -> InlineKeyboardMarkup:
    cur_day = datetime.date.today()

    tasks_today_button = InlineKeyboardButton(
        text=TASKS_LEXICON["tasks_today"],
        callback_data=f"calendar_get_{cur_day.year}-{cur_day.month}-{cur_day.day}"
    )
    tasks_from_day_button = InlineKeyboardButton(
        text=TASKS_LEXICON["tasks_from_day"],
        callback_data="get_tasks_from_day"
    )
    all_tasks_button = InlineKeyboardButton(
        text=TASKS_LEXICON["all_tasks"],
        callback_data="show_tasks_all"
    )
    active_tasks_button = InlineKeyboardButton(
        text=TASKS_LEXICON["active_tasks"],
        callback_data="show_tasks_active"
    )
    completed_tasks_button = InlineKeyboardButton(
        text=TASKS_LEXICON["completed_tasks"],
        callback_data="show_tasks_completed"
    )
    exit_button = InlineKeyboardButton(
        text=UNIVERSAL_LEXICON["exit"],
        callback_data="exit"
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [tasks_today_button],
            [tasks_from_day_button],
            [all_tasks_button],
            [active_tasks_button],
            [completed_tasks_button],
            [exit_button]
        ]
    )


def task_edit_keyboard(task_id: int) -> InlineKeyboardMarkup:
    edit_name_button = InlineKeyboardButton(
        text=TASKS_LEXICON["edit_name"],
        callback_data="edit_task_name"
    )
    edit_description_button = InlineKeyboardButton(
        text=TASKS_LEXICON["edit_description"],
        callback_data="edit_task_description"
    )
    edit_priority_button = InlineKeyboardButton(
        text=TASKS_LEXICON["edit_priority"],
        callback_data="edit_task_priority"
    )
    edit_category_button = InlineKeyboardButton(
        text=TASKS_LEXICON["edit_category"],
        callback_data="edit_task_category"
    )
    edit_date_button = InlineKeyboardButton(
        text=TASKS_LEXICON["edit_date"],
        callback_data="edit_task_date"
    )
    back_to_task_button = InlineKeyboardButton(
        text=TASKS_LEXICON["back_to_task"],
        callback_data=f"get_task_{task_id}"
    )
    exit_button = InlineKeyboardButton(
        text=UNIVERSAL_LEXICON["exit"],
        callback_data="exit"
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [edit_name_button],
            [edit_description_button],
            [edit_priority_button],
            [edit_category_button],
            [edit_date_button],
            [back_to_task_button],
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

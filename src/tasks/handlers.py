import datetime

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state

from .services import TaskService
from .lexicon import LEXICON as TASKS_LEXICON, LEXICON_COMMANDS as TASKS_LEXICON_COMMANDS, create_task_about_text
from .keyboards import show_tasks_keyboard, add_description_keyboard, select_priority_keyboard, \
    tasks_calendar_keyboard, select_month_keyboard, tasks_menu_keyboard, task_about_keyboard, yes_no_keyboard, \
    task_edit_keyboard
from .states import TaskState

from src.categories.handlers import category_service
from src.categories.keyboards import all_categories_keyboard_for_tasks

from utils.middleware import AuthMiddleware
from utils.utils import priority_converter, set_edited_task_data, format_date

from src.users.handlers import router as user_router

router = Router()
router.message.middleware(AuthMiddleware())
router.callback_query.middleware(AuthMiddleware())
task_service = TaskService()


@router.callback_query(F.data == "tasks_menu")
async def show_tasks_menu(callback: CallbackQuery):
    await callback.message.answer(
        text=TASKS_LEXICON["tasks_menu"],
        reply_markup=tasks_menu_keyboard()
    )


@router.callback_query(F.data[:15] == "edit_task_menu_")
async def show_edit_task_menu(callback: CallbackQuery, state: FSMContext):
    task_id = int(callback.data[15:])
    await state.update_data(task_id=task_id)
    await callback.message.edit_text(
        text=TASKS_LEXICON["edit_task_menu"],
        reply_markup=task_edit_keyboard(task_id)
    )


@router.callback_query(F.data == "edit_task_name")
async def edit_task_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TaskState.edit_name)
    await callback.message.edit_text(text=TASKS_LEXICON["get_name"])


@router.message(StateFilter(TaskState.edit_name))
async def set_task_name(message: Message, state: FSMContext):
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    task = await task_service.get_task_by_id(task_id, user_data["access_token"])

    data = set_edited_task_data(task, "name", message.text)

    task = await task_service.edit_task(task_id, data, user_data["access_token"])
    task_category = await category_service.get_category(task["category_id"], user_data["access_token"])

    await state.set_state(default_state)
    await message.answer(text=TASKS_LEXICON["name_edited"])
    await message.answer(
        text=create_task_about_text(task, task_category), parse_mode="Markdown",
        reply_markup=task_about_keyboard(task["id"], task["completed"])
    )


@router.callback_query(F.data == "edit_task_description")
async def edit_description(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TaskState.edit_description)
    await callback.message.edit_text(
        text=TASKS_LEXICON["get_description"],
        reply_markup=add_description_keyboard()
    )


@router.callback_query(F.data == "no_add_description", StateFilter(TaskState.edit_description))
async def no_edit_description(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    task = await task_service.get_task_by_id(user_data["task_id"], user_data["access_token"])
    task_category = await category_service.get_category(task["category_id"], user_data["access_token"])

    await state.set_state(default_state)
    await callback.message.edit_text(
        text=create_task_about_text(task, task_category), parse_mode="Markdown",
        reply_markup=task_about_keyboard(task["id"], task["completed"])
    )


@router.message(StateFilter(TaskState.edit_description))
async def set_new_task_description(message: Message, state: FSMContext):
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    task = await task_service.get_task_by_id(task_id, user_data["access_token"])

    data = set_edited_task_data(task, "description", message.text)
    task = await task_service.edit_task(task_id, data, user_data["access_token"])
    task_category = await category_service.get_category(task["category_id"], user_data["access_token"])

    await state.set_state(default_state)
    await message.answer(text=TASKS_LEXICON["description_edited"])
    await message.answer(
        text=create_task_about_text(task, task_category), parse_mode="Markdown",
        reply_markup=task_about_keyboard(task["id"], task["completed"])
    )


@router.callback_query(F.data == "edit_task_priority")
async def edit_priority(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TaskState.edit_priority)
    await callback.message.edit_text(
        text=TASKS_LEXICON["get_priority"],
        reply_markup=select_priority_keyboard()
    )


@router.callback_query(F.data[-8:] == "priority", StateFilter(TaskState.edit_priority))
async def set_new_task_priority(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    task = await task_service.get_task_by_id(task_id, user_data["access_token"])

    data = set_edited_task_data(task, "priority", priority_converter[callback.data[:-9]])
    task = await task_service.edit_task(task_id, data, user_data["access_token"])
    task_category = await category_service.get_category(task["category_id"], user_data["access_token"])

    await state.set_state(default_state)
    await callback.message.edit_text(text=TASKS_LEXICON["priority_edited"])
    await callback.message.answer(
        text=create_task_about_text(task, task_category), parse_mode="Markdown",
        reply_markup=task_about_keyboard(task["id"], task["completed"])
    )


@router.callback_query(F.data[:20] == "show_category_tasks_")
async def get_tasks_from_category(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data[20:])
    user_data = await state.get_data()

    category = await category_service.get_category(category_id, user_data["access_token"])
    tasks = category["tasks"]
    await callback.message.edit_text(
        text=TASKS_LEXICON["tasks_from_category"].format(name=category["name"]), parse_mode="Markdown",
        reply_markup=show_tasks_keyboard(tasks)
    )


@router.callback_query(F.data == "edit_task_category")
async def edit_task_category(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TaskState.edit_category)
    user_data = await state.get_data()
    categories = await category_service.get_categories(user_data["access_token"])

    await callback.message.edit_text(
        text=TASKS_LEXICON["get_category"],
        reply_markup=all_categories_keyboard_for_tasks(categories)
    )


@router.callback_query(F.data[:13] == "get_category_", StateFilter(TaskState.edit_category))
async def set_new_task_category(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    task = await task_service.get_task_by_id(task_id, user_data["access_token"])

    data = set_edited_task_data(task, "category_id", int(callback.data[13:]))
    task = await task_service.edit_task(task_id, data, user_data["access_token"])
    task_category = await category_service.get_category(task["category_id"], user_data["access_token"])

    await state.set_state(default_state)
    await callback.message.edit_text(text=TASKS_LEXICON["category_edited"])
    await callback.message.answer(
        text=create_task_about_text(task, task_category), parse_mode="Markdown",
        reply_markup=task_about_keyboard(task["id"], task["completed"])
    )


@router.callback_query(F.data == "edit_task_date")
async def edit_date(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TaskState.edit_date)
    await callback.message.edit_text(
        text=TASKS_LEXICON["get_date"],
        reply_markup=tasks_calendar_keyboard()
    )


@router.callback_query(F.data[:13] == "calendar_get_", StateFilter(TaskState.edit_date))
async def set_new_task_date(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    task = await task_service.get_task_by_id(task_id, user_data["access_token"])

    data = set_edited_task_data(task, "date", format_date(callback.data[13:]))
    task = await task_service.edit_task(task_id, data, user_data["access_token"])
    task_category = await category_service.get_category(task["category_id"], user_data["access_token"])

    await state.set_state(default_state)
    await callback.message.edit_text(text=TASKS_LEXICON["date_edited"])
    await callback.message.answer(
        text=create_task_about_text(task, task_category), parse_mode="Markdown",
        reply_markup=task_about_keyboard(task["id"], task["completed"])
    )


@router.message(Command(commands=["all_tasks", "active_tasks", "completed_tasks"]), StateFilter(default_state))
async def get_tasks(message: Message, state: FSMContext):
    user_data = await state.get_data()

    tasks = await task_service.get_all_tasks(user_data["access_token"])
    if message.text == "/active_tasks":
        tasks = [task for task in tasks if not task["completed"]]
    elif message.text == "/completed_tasks":
        tasks = [task for task in tasks if task["completed"]]
    tasks.sort(key=lambda x: datetime.datetime.strptime(x["date"], '%Y-%m-%d'), reverse=True)

    await message.answer(
        text=TASKS_LEXICON_COMMANDS[message.text],
        reply_markup=show_tasks_keyboard(tasks)
    )


@router.callback_query(F.data[:9] == "get_task_")
async def get_task_about(callback: CallbackQuery, state: FSMContext):
    task_id = int(callback.data[9:])
    user_data = await state.get_data()

    task = await task_service.get_task_by_id(task_id, user_data["access_token"])
    task_category = await category_service.get_category(task["category_id"], user_data["access_token"])

    await callback.message.edit_text(
        text=create_task_about_text(task, task_category), parse_mode="Markdown",
        reply_markup=task_about_keyboard(task["id"], task["completed"])
    )


@router.callback_query(F.data[:11] == "show_tasks_")
async def get_tasks(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    tasks = await task_service.get_all_tasks(user_data["access_token"])
    if callback.data == "show_tasks_active":
        tasks = [task for task in tasks if not task["completed"]]
    elif callback.data == "show_tasks_completed":
        tasks = [task for task in tasks if task["completed"]]
    tasks.sort(key=lambda x: datetime.datetime.strptime(x["date"], '%Y-%m-%d'), reverse=True)

    await callback.message.edit_text(
        text=TASKS_LEXICON_COMMANDS[f"/{callback.data[11:]}_tasks"],
        reply_markup=show_tasks_keyboard(tasks)
    )


@router.callback_query(F.data[:17] == "edit_task_status_")
async def edit_task_status(callback: CallbackQuery, state: FSMContext):
    task_id = int(callback.data[17:])
    user_data = await state.get_data()

    task = await task_service.change_task_status(task_id, user_data["access_token"])
    task_category = await category_service.get_category(task["category_id"], user_data["access_token"])
    await callback.message.edit_text(text=TASKS_LEXICON["task_status_changed"])
    await callback.message.answer(
        text=create_task_about_text(task, task_category), parse_mode="Markdown",
        reply_markup=task_about_keyboard(task["id"], task["completed"])
    )


@router.callback_query(F.data[:12] == "delete_task_")
async def start_delete_task(callback: CallbackQuery, state: FSMContext):
    task_id = int(callback.data[12:])
    await state.update_data(task_id=task_id)
    await state.set_state(TaskState.delete_task)
    await callback.message.edit_text(
        text=TASKS_LEXICON["delete_task_confirmation"],
        reply_markup=yes_no_keyboard()
    )


@router.callback_query(F.data == "no", StateFilter(TaskState.delete_task))
async def cancel_delete_task(callback: CallbackQuery, state: FSMContext):
    await state.set_state(default_state)
    user_data = await state.get_data()

    task = await task_service.get_task_by_id(user_data["task_id"], user_data["access_token"])
    task_category = await category_service.get_category(task["category_id"], user_data["access_token"])

    await callback.message.edit_text(text=TASKS_LEXICON["cancel_delete"])
    await callback.message.answer(
        text=create_task_about_text(task, task_category), parse_mode="Markdown",
        reply_markup=task_about_keyboard(task["id"], task["completed"])
    )


@router.callback_query(F.data == "yes", StateFilter(TaskState.delete_task))
async def delete_task(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    await task_service.delete_task(user_data["task_id"], user_data["access_token"])
    await callback.message.edit_text(text=TASKS_LEXICON["task_deleted"])
    await state.set_state(default_state)


@router.callback_query(F.data == "get_tasks_from_day")
async def select_day_for_show_task(callback: CallbackQuery, state: FSMContext):
    await state.set_state(default_state)
    await callback.message.edit_text(
        text=TASKS_LEXICON["get_date"],
        reply_markup=tasks_calendar_keyboard()
    )


@router.callback_query(F.data[:13] == "calendar_get_")
async def show_task_from_day(callback: CallbackQuery, state: FSMContext):
    date = callback.data[13:]
    user_data = await state.get_data()
    tasks = [task for task in await task_service.get_all_tasks(user_data["access_token"]) if task["date"] == date]

    await callback.message.edit_text(
        text=TASKS_LEXICON["show_tasks_from_day"].format(date=date),
        reply_markup=show_tasks_keyboard(tasks)
    )


@router.message(Command(commands="create_task"), StateFilter(default_state))
async def create_task(message: Message, state: FSMContext):
    user_data = await state.get_data()
    categories = await category_service.get_categories(user_data["access_token"])
    await message.answer(
        text=TASKS_LEXICON_COMMANDS[message.text],
        reply_markup=all_categories_keyboard_for_tasks(categories)
    )

    await state.set_state(TaskState.get_category)


@router.callback_query(F.data[:13] == "get_category_", StateFilter(TaskState.get_category))
async def set_task_category(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    category = await category_service.get_category(int(callback.data[13:]), user_data["access_token"])
    await state.update_data(task_category_id=category["id"])

    await callback.message.edit_text(text=TASKS_LEXICON["get_name"], parse_mode="Markdown")
    await state.set_state(TaskState.get_name)


@router.message(StateFilter(TaskState.get_name))
async def set_task_name(message: Message, state: FSMContext):
    await state.update_data(task_name=message.text)

    await message.answer(
        text=TASKS_LEXICON["get_description"], parse_mode="Markdown",
        reply_markup=add_description_keyboard()
    )
    await state.set_state(TaskState.get_description)


@router.callback_query(F.data == "no_add_description", StateFilter(TaskState.get_description))
async def no_add_description(callback: CallbackQuery, state: FSMContext):
    await state.update_data(task_description="")
    await callback.message.edit_text(
        text=TASKS_LEXICON["get_priority"],
        reply_markup=select_priority_keyboard()
    )
    await state.set_state(TaskState.get_priority)


@router.message(StateFilter(TaskState.get_description))
async def set_task_description(message: Message, state: FSMContext):
    await state.update_data(task_description=message.text)
    await message.answer(
        text=TASKS_LEXICON["get_priority"],
        reply_markup=select_priority_keyboard()
    )
    await state.set_state(TaskState.get_priority)


@router.callback_query(F.data[-8:] == "priority", StateFilter(TaskState.get_priority))
async def set_task_priority(callback: CallbackQuery, state: FSMContext):
    await state.update_data(task_priority=priority_converter[callback.data[:-9]])
    await callback.message.edit_text(
        text=TASKS_LEXICON["get_date"],
        reply_markup=tasks_calendar_keyboard()
    )
    await state.set_state(TaskState.get_date)


@router.callback_query(F.data[:13] == "calendar_get_", StateFilter(TaskState.get_date))
async def set_task_date(callback: CallbackQuery, state: FSMContext):
    await state.update_data(task_date=callback.data[13:])
    user_data = await state.get_data()

    request_body = {
        "name": user_data["task_name"],
        "description": user_data["task_description"],
        "priority": user_data["task_priority"],
        "category_id": user_data["task_category_id"],
        "date": format_date(user_data["task_date"]),

    }

    task = await task_service.create_task(request_body, user_data["access_token"])
    task_category = await category_service.get_category(task["category_id"], user_data["access_token"])

    await callback.message.edit_text(text=TASKS_LEXICON["successful_create"])
    await callback.message.answer(
        text=create_task_about_text(task, task_category), parse_mode="Markdown",
        reply_markup=task_about_keyboard(task["id"], task["completed"])
    )
    await state.set_state(default_state)


@user_router.callback_query(F.data[:14] == "calendar_page_")
async def change_tasks_keyboard_page(callback: CallbackQuery):
    year = int(callback.data[14:18])
    month = int(callback.data[19:])
    await callback.message.edit_text(
        text=TASKS_LEXICON["get_date"],
        reply_markup=tasks_calendar_keyboard(datetime.date(year, month, 1))
    )


@user_router.callback_query(F.data[:21] == "calendar_select_year_")
async def change_tasks_keyboard_year(callback: CallbackQuery, state: FSMContext):
    await state.update_data(month=int(callback.data[21:]), state=await state.get_state())
    await callback.message.edit_text(text=TASKS_LEXICON["get_year"])
    await state.set_state(TaskState.get_year)


@user_router.message(StateFilter(TaskState.get_year))
async def set_year(message: Message, state: FSMContext):
    user_data = await state.get_data()
    month = user_data["month"]
    year = int(message.text)
    await state.set_state(user_data["state"])
    await message.answer(
        text=TASKS_LEXICON["get_date"],
        reply_markup=tasks_calendar_keyboard(datetime.date(year, month, 1))
    )


@router.callback_query(F.data[:22] == "calendar_select_month_")
async def change_tasks_keyboard_month(callback: CallbackQuery, state: FSMContext):
    await state.update_data(year=int(callback.data[22:]), state=await state.get_state())
    await callback.message.edit_text(
        text=TASKS_LEXICON["get_month"],
        reply_markup=select_month_keyboard()
    )
    await state.set_state(TaskState.get_month)


@router.callback_query(F.data[:10] == "get_month_", StateFilter(TaskState.get_month))
async def set_month(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    year = user_data["year"]
    month = int(callback.data[10:])
    await state.set_state(user_data["state"])
    await callback.message.edit_text(
        text=TASKS_LEXICON["get_date"],
        reply_markup=tasks_calendar_keyboard(datetime.date(year, month, 1))
    )

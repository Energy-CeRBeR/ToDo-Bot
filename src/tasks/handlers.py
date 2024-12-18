import datetime

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state

from .services import TaskService
from .lexicon import LEXICON as TASKS_LEXICON, LEXICON_COMMANDS as TASKS_LEXICON_COMMANDS
from .keyboards import show_tasks_keyboard, add_description_keyboard, select_priority_keyboard, \
    tasks_calendar_keyboard, select_month_keyboard, tasks_menu_keyboard, task_about_keyboard
from .states import TaskState

from src.categories.handlers import category_service
from src.categories.keyboards import all_categories_keyboard_for_tasks

from utils.middleware import AuthMiddleware
from utils.utils import priority_converter, inverse_priority_converter

from src.users.handlers import router as user_router

router = Router()
router.message.middleware(AuthMiddleware())
router.callback_query.middleware(AuthMiddleware())
task_service = TaskService()


@user_router.message(Command(commands="test_calendar"))
async def test_calendar(message: Message):
    await message.answer(
        text=TASKS_LEXICON["get_date"],
        reply_markup=tasks_calendar_keyboard()
    )


@router.callback_query(F.data == "tasks_menu", StateFilter(default_state))
async def show_tasks_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=TASKS_LEXICON["tasks_menu"],
        reply_markup=tasks_menu_keyboard()
    )
    await state.set_state(TaskState.show_task)


@router.message(Command(commands=["all_tasks", "active_tasks", "completed_tasks"]), StateFilter(default_state))
async def get_tasks(message: Message, state: FSMContext):
    user_data = await state.get_data()

    tasks = await task_service.get_all_tasks(user_data["access_token"])
    if message.text == "/active_tasks":
        tasks = [task for task in tasks if not task["completed"]]
    elif message.text == "/completed_tasks":
        tasks = [task for task in tasks if task["completed"]]
    tasks.sort(key=lambda x: x["date"], reverse=True)

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

    name = task["name"]
    description = task["description"] if task["description"] else TASKS_LEXICON["no_description"]
    priority = inverse_priority_converter[task["priority"]]
    category = task_category["name"]
    status = TASKS_LEXICON["check_status"][int(task["completed"])]
    date = task["date"]

    await callback.message.edit_text(
        text=TASKS_LEXICON["show_task_about"].format(
            name=name, description=description, priority=priority, category=category, status=status, date=date
        ), parse_mode="Markdown",
        reply_markup=task_about_keyboard(task["id"], task["completed"])
    )


@router.callback_query(F.data[:11] == "show_tasks_", StateFilter(TaskState.show_task))
async def get_tasks(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    tasks = await task_service.get_all_tasks(user_data["access_token"])
    if callback.data == "show_tasks_active":
        tasks = [task for task in tasks if not task["completed"]]
    elif callback.data == "show_tasks_completed":
        tasks = [task for task in tasks if task["completed"]]
    tasks.sort(key=lambda x: x["date"], reverse=True)

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

    name = task["name"]
    description = task["description"] if task["description"] else TASKS_LEXICON["no_description"]
    priority = inverse_priority_converter[task["priority"]]
    category = task_category["name"]
    status = TASKS_LEXICON["check_status"][int(task["completed"])]
    date = task["date"]

    await callback.message.edit_text(text=TASKS_LEXICON["task_status_changed"])
    await callback.message.answer(
        text=TASKS_LEXICON["show_task_about"].format(
            name=name, description=description, priority=priority, category=category, status=status, date=date
        ), parse_mode="Markdown",
        reply_markup=task_about_keyboard(task["id"], task["completed"])
    )


@router.callback_query(F.data == "get_tasks_from_day", StateFilter(TaskState.show_task))
async def select_day_for_show_task(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=TASKS_LEXICON["get_date"],
        reply_markup=tasks_calendar_keyboard()
    )
    await state.set_state(TaskState.show_task)


@router.callback_query(F.data[:13] == "calendar_get_", StateFilter(TaskState.show_task))
async def show_task_from_day(callback: CallbackQuery, state: FSMContext):
    date = callback.data[13:]
    user_data = await state.get_data()
    tasks = [task for task in await task_service.get_all_tasks(user_data["access_token"]) if task["date"] == date]

    await callback.message.edit_text(
        text=TASKS_LEXICON["show_tasks_from_day"].format(date=date),
        reply_markup=show_tasks_keyboard(tasks)
    )
    await state.set_state(default_state)


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
        "date": user_data["task_date"],

    }

    await task_service.create_task(request_body, user_data["access_token"])
    await callback.message.edit_text(
        text=TASKS_LEXICON["successful_create"],
        # reply_markup=tasks_calendar_keyboard(selected_date=state.get_data()["task_date"])
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

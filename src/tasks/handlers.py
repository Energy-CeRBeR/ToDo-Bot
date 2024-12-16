import datetime

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state

from .services import TaskService
from .lexicon import LEXICON as TASKS_LEXICON, LEXICON_COMMANDS as TASKS_LEXICON_COMMANDS
from .keyboards import all_tasks_keyboard, add_description_keyboard, select_priority_keyboard, \
    tasks_calendar_keyboard, select_month_keyboard
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
async def set_task_date(message: Message):
    await message.answer(
        text=TASKS_LEXICON["get_date"],
        reply_markup=tasks_calendar_keyboard()
    )


@router.message(Command(commands="all_tasks"), StateFilter(default_state))
async def get_categories(message: Message, state: FSMContext):
    user_data = await state.get_data()
    tasks = await task_service.get_all_tasks(user_data["access_token"])
    await message.answer(
        text=TASKS_LEXICON_COMMANDS[message.text],
        reply_markup=all_tasks_keyboard(tasks)
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
    await state.update_data(task_date=datetime.date.fromisoformat(callback.data[13:]))
    await callback.message.edit_text(
        text=TASKS_LEXICON["successful_create"],
        # reply_markup=tasks_calendar_keyboard(selected_date=state.get_data()["task_date"])
    )
    await state.set_state(default_state)


@user_router.callback_query(F.data[:14] == "calendar_page_")
async def change_tasks_keyboard_page(callback: CallbackQuery):
    year = int(callback.data[14:18])
    month = int(callback.data[19:])
    print(month)
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


@user_router.callback_query(F.data[:22] == "calendar_select_month_")
async def change_tasks_keyboard_month(callback: CallbackQuery, state: FSMContext):
    await state.update_data(year=int(callback.data[22:]), state=await state.get_state())
    await callback.message.edit_text(
        text=TASKS_LEXICON["get_month"],
        reply_markup=select_month_keyboard()
    )
    await state.set_state(TaskState.get_month)


@user_router.callback_query(F.data[:10] == "get_month_", StateFilter(TaskState.get_month))
async def set_month(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    year = user_data["year"]
    month = int(callback.data[10:])
    await state.set_state(user_data["state"])
    await callback.message.edit_text(
        text=TASKS_LEXICON["get_date"],
        reply_markup=tasks_calendar_keyboard(datetime.date(year, month, 1))
    )

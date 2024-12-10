from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state

from utils.middleware import AuthMiddleware
from .services import CategoryService
from .lexicon import LEXICON as CATEGORIES_LEXICON, LEXICON_COMMANDS as CATEGORIES_LEXICON_COMMANDS
from .keyboards import all_categories_keyboard, show_category_keyboard, choose_category_color
from .states import CreateCategoryState

router = Router()
router.message.middleware(AuthMiddleware())
router.callback_query.middleware(AuthMiddleware())
category_service = CategoryService()


@router.message(Command(commands="categories"), StateFilter(default_state))
async def get_categories(message: Message, state: FSMContext):
    user_data = await state.get_data()
    categories = await category_service.get_categories(user_data["access_token"])
    await message.answer(
        text=CATEGORIES_LEXICON_COMMANDS[message.text],
        reply_markup=all_categories_keyboard(categories)
    )


@router.callback_query(F.data == "show_categories", StateFilter(default_state))
async def get_categories(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    categories = await category_service.get_categories(user_data["access_token"])
    await callback.message.edit_text(
        text=CATEGORIES_LEXICON_COMMANDS["/categories"],
        reply_markup=all_categories_keyboard(categories)
    )


@router.callback_query(F.data[:13] == "get_category_", StateFilter(default_state))
async def get_category(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    category = await category_service.get_category(int(callback.data[13:]), user_data["access_token"])
    await callback.message.edit_text(
        text=CATEGORIES_LEXICON["category_info"].format(name=category["name"]),
        parse_mode="Markdown",
        reply_markup=show_category_keyboard(category["id"])
    )


@router.message(Command(commands="create_category"), StateFilter(default_state))
async def create_category(message: Message, state: FSMContext):
    await message.answer(text=CATEGORIES_LEXICON_COMMANDS[message.text])
    await state.set_state(CreateCategoryState.get_name)


@router.message(StateFilter(CreateCategoryState.get_name))
async def get_category_name(message: Message, state: FSMContext):
    await state.update_data(category_name=message.text)
    await message.answer(
        text=CATEGORIES_LEXICON["choose_category_color"],
        reply_markup=choose_category_color()
    )
    await state.set_state(CreateCategoryState.get_color)


@router.callback_query(F.data[:15] == "category_color_", StateFilter(CreateCategoryState.get_color))
async def get_category_color(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    new_category = await category_service.create_category(
        user_data["category_name"], callback.data[15:], user_data["access_token"]
    )
    await state.set_state(default_state)
    await callback.message.edit_text(
        text=CATEGORIES_LEXICON["successful_created"].format(name=new_category["name"]),
        parse_mode="Markdown",
        reply_markup=show_category_keyboard(new_category["id"])
    )

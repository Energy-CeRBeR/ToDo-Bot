from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.middleware import AuthMiddleware
from .services import CategoryService
from .lexicon import LEXICON as CATEGORIES_LEXICON, LEXICON_COMMANDS as CATEGORIES_LEXICON_COMMANDS
from .keyboards import all_categories_keyboard

router = Router()
router.message.middleware(AuthMiddleware())
router.callback_query.middleware(AuthMiddleware())
category_service = CategoryService()


@router.message(Command(commands="categories"))
async def get_categories(message: Message, state: FSMContext):
    user_data = await state.get_data()
    categories = await category_service.get_categories(user_data["access_token"])
    await message.answer(
        text=CATEGORIES_LEXICON_COMMANDS[message.text],
        reply_markup=all_categories_keyboard(categories)
    )


@router.callback_query(F.data == "show_categories")
async def get_categories(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    categories = await category_service.get_categories(user_data["access_token"])
    await callback.message.answer(
        text=CATEGORIES_LEXICON_COMMANDS["/categories"],
        reply_markup=all_categories_keyboard(categories)
    )


@router.callback_query(F.data[:13] == "get_category_")
async def get_category(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    category = await category_service.get_category(int(callback.data[13:]), user_data["access_token"])
    print(category)


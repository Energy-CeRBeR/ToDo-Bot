from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state

from .services import CategoryService
from .lexicon import LEXICON as CATEGORIES_LEXICON, LEXICON_COMMANDS as CATEGORIES_LEXICON_COMMANDS
from .keyboards import all_categories_keyboard, category_about_keyboard, yes_no_keyboard
from .states import CategoryState

from utils.middleware import AuthMiddleware
from utils.universal_lexicon import LEXICON as UNIVERSAL_LEXICON
from config_data.config import MAX_OBJECTS_ON_PAGE

router = Router()
router.message.middleware(AuthMiddleware())
router.callback_query.middleware(AuthMiddleware())
category_service = CategoryService()


@router.message(Command(commands="categories"), StateFilter(default_state))
async def get_categories(message: Message, state: FSMContext):
    user_data = await state.get_data()
    categories = await category_service.get_categories_without_base(user_data["access_token"])
    pages = len(categories) // MAX_OBJECTS_ON_PAGE + int(len(categories) % MAX_OBJECTS_ON_PAGE != 0)

    await state.update_data(categories_list=categories, categories_pages=pages, cur_page=1)
    await message.answer(
        text=CATEGORIES_LEXICON_COMMANDS[message.text].format(page=1, pages=pages),
        reply_markup=all_categories_keyboard(categories[:MAX_OBJECTS_ON_PAGE])
    )


@router.callback_query(lambda c: c.data in ("show_categories", "back_to_categories"), StateFilter(default_state))
async def get_categories(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    categories = await category_service.get_categories_without_base(user_data["access_token"])
    pages = len(categories) // MAX_OBJECTS_ON_PAGE + int(len(categories) % MAX_OBJECTS_ON_PAGE != 0)

    await state.update_data(categories_list=categories, categories_pages=pages, cur_page=1)
    if callback.data == "show_categories":
        await callback.message.answer(
            text=CATEGORIES_LEXICON_COMMANDS["/categories"].format(page=1, pages=pages),
            reply_markup=all_categories_keyboard(categories[:MAX_OBJECTS_ON_PAGE])
        )
    else:
        await callback.message.edit_text(
            text=CATEGORIES_LEXICON_COMMANDS["/categories"].format(page=1, pages=pages),
            reply_markup=all_categories_keyboard(categories[:MAX_OBJECTS_ON_PAGE])
        )


@router.callback_query(lambda c: c.data in ("next_cat_page", "prev_cat_page"))
async def next_cat_page(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    categories = user_data["categories_list"]
    pages = user_data["categories_pages"]
    cur_page = user_data["cur_page"]

    if callback.data == "next_cat_page":
        if cur_page < pages:
            cur_page += 1
            await state.update_data(cur_page=cur_page)
        else:
            await callback.answer(
                text=UNIVERSAL_LEXICON["no_next_page"],
                reply_markup=all_categories_keyboard(
                    categories[(cur_page - 1) * MAX_OBJECTS_ON_PAGE: cur_page * MAX_OBJECTS_ON_PAGE]
                )
            )

    else:
        if cur_page > 1:
            cur_page -= 1
            await state.update_data(cur_page=cur_page)
        else:
            await callback.answer(
                text=UNIVERSAL_LEXICON["no_prev_page"],
                reply_markup=all_categories_keyboard(
                    categories[(cur_page - 1) * MAX_OBJECTS_ON_PAGE: cur_page * MAX_OBJECTS_ON_PAGE]
                )
            )

    await callback.message.edit_text(
        text=CATEGORIES_LEXICON_COMMANDS["/categories"].format(page=cur_page, pages=pages),
        reply_markup=all_categories_keyboard(
            categories[(cur_page - 1) * MAX_OBJECTS_ON_PAGE: cur_page * MAX_OBJECTS_ON_PAGE]
        )
    )


@router.callback_query(F.data[:13] == "get_category_")
async def get_category(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    category = await category_service.get_category(int(callback.data[13:]), user_data["access_token"])
    await callback.message.edit_text(
        text=CATEGORIES_LEXICON["category_info"].format(name=category["name"]),
        parse_mode="Markdown",
        reply_markup=category_about_keyboard(category["id"])
    )


@router.message(Command(commands="create_category"))
async def start_create_category(message: Message, state: FSMContext):
    await message.answer(text=CATEGORIES_LEXICON_COMMANDS[message.text])
    await state.set_state(CategoryState.get_name)


@router.message(StateFilter(CategoryState.get_name))
async def finish_create_category(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await state.set_state(default_state)

    new_category = await category_service.create_category(message.text, user_data["access_token"])
    await message.answer(
        text=CATEGORIES_LEXICON["successful_created"].format(name=new_category["name"]),
        parse_mode="Markdown",
        reply_markup=category_about_keyboard(new_category["id"])
    )


@router.callback_query(F.data[:19] == "edit_category_name_")
async def edit_category_name(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    category_id = int(callback.data[19:])
    category = await category_service.get_category(category_id, user_data["access_token"])
    await state.update_data(category_id=category_id, color=category["color"])

    await state.set_state(CategoryState.get_new_name)
    await callback.message.edit_text(
        text=CATEGORIES_LEXICON["get_new_name"].format(name=category["name"]), parse_mode="Markdown"
    )


@router.message(StateFilter(CategoryState.get_new_name))
async def set_new_name(message: Message, state: FSMContext):
    user_data = await state.get_data()
    new_category_data = {"name": message.text, "color": user_data["color"]}
    await category_service.edit_category(user_data["category_id"], new_category_data, user_data["access_token"])

    await state.set_state(default_state)
    await message.answer(
        text=CATEGORIES_LEXICON["successful_updated"].format(name=message.text),
        parse_mode="Markdown",
        reply_markup=category_about_keyboard(user_data["category_id"])
    )


@router.callback_query(F.data[:16] == "delete_category_")
async def start_delete_category(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data[16:])
    await state.update_data(category_id=category_id)
    await state.set_state(CategoryState.delete_category)
    await callback.message.edit_text(
        text=CATEGORIES_LEXICON["delete_category_confirmation"],
        reply_markup=yes_no_keyboard()
    )


@router.callback_query(F.data == "no", StateFilter(CategoryState.delete_category))
async def cancel_delete_category(callback: CallbackQuery, state: FSMContext):
    await state.set_state(default_state)
    user_data = await state.get_data()

    category = await category_service.get_category(user_data["category_id"], user_data["access_token"])
    await callback.message.edit_text(text=CATEGORIES_LEXICON["cancel_delete"])
    await callback.message.answer(
        text=CATEGORIES_LEXICON["category_info"].format(name=category["name"]),
        parse_mode="Markdown",
        reply_markup=category_about_keyboard(category["id"])
    )


@router.callback_query(F.data == "yes", StateFilter(CategoryState.delete_category))
async def delete_category(callback: CallbackQuery, state: FSMContext):
    await state.set_state(default_state)
    user_data = await state.get_data()

    await category_service.delete_category(user_data["category_id"], user_data["access_token"])
    await callback.message.edit_text(text=CATEGORIES_LEXICON["category_deleted"])

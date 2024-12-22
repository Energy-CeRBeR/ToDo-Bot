from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from .states import AuthorizeState
from .lexicon import LEXICON_COMMANDS as USER_LEXICON_COMMANDS, LEXICON as USER_LEXICON
from .services import UserService
from .keyboards import profile_keyboard, yes_no_keyboard

router = Router()
user_service = UserService()


@router.message(CommandStart(), StateFilter(default_state))
async def start_bot(message: Message):
    await message.answer(USER_LEXICON_COMMANDS[message.text], parse_mode="Markdown")


@router.message(Command(commands="cerber"))
async def cerber_auth(message: Message, state: FSMContext):
    tokens = await user_service.login_user("cerber17", "energy_cerber")
    if tokens:
        await state.update_data(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"]
        )

        user_data = await state.get_data()
        user_dict = await user_service.get_current_user(user_data.setdefault("access_token", "default"))
        await message.answer(
            text=USER_LEXICON_COMMANDS["/profile"].format(
                name=user_dict["name"], surname=user_dict["surname"], email=user_dict["email"]
            ), parse_mode="Markdown",
            reply_markup=profile_keyboard()
        )

    else:
        await message.answer(text=USER_LEXICON["invalid_auth"])


@router.message(Command(commands="help"), StateFilter(default_state))
async def help_info(message: Message):
    await message.answer(text=USER_LEXICON_COMMANDS[message.text], parse_mode="Markdown")


@router.message(Command(commands="auth"), StateFilter(default_state))
async def start_auth(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_dict = await user_service.get_current_user(user_data.setdefault("access_token", "default"))

    if user_dict:
        await message.answer(text=USER_LEXICON_COMMANDS[message.text]["already_authorized"])
    else:
        await message.answer(text=USER_LEXICON_COMMANDS[message.text]["not_authorized"])
        await state.set_state(AuthorizeState.get_email)


@router.message(StateFilter(AuthorizeState.get_email))
async def get_email(message: Message, state: FSMContext):
    email = message.text.strip()
    await message.delete()
    await state.update_data(email=email)
    await message.answer(text=USER_LEXICON["get_password"])
    await state.set_state(AuthorizeState.get_password)


@router.message(StateFilter(AuthorizeState.get_password))
async def get_password(message: Message, state: FSMContext):
    await state.set_state(default_state)
    data = await state.get_data()
    email = data["email"]
    password = message.text.strip()
    await message.delete()

    tokens = await user_service.login_user(email, password)
    if tokens:
        await state.update_data(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"]
        )

        user_data = await state.get_data()
        user_dict = await user_service.get_current_user(user_data.setdefault("access_token", "default"))
        await message.answer(
            text=USER_LEXICON_COMMANDS["/profile"].format(
                name=user_dict["name"], surname=user_dict["surname"], email=user_dict["email"]
            ), parse_mode="Markdown",
            reply_markup=profile_keyboard()
        )

    else:
        await message.answer(text=USER_LEXICON["invalid_auth"])


@router.message(Command(commands="profile"), StateFilter(default_state))
async def show_profile(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_dict = await user_service.get_current_user(user_data.setdefault("access_token", "default"))

    if user_dict:
        await message.answer(
            text=USER_LEXICON_COMMANDS[message.text].format(
                name=user_dict["name"], surname=user_dict["surname"], email=user_dict["email"]
            ), parse_mode="Markdown",
            reply_markup=profile_keyboard()
        )
    else:
        await message.answer(text=USER_LEXICON["not_auth"])


@router.message(Command(commands="logout"), StateFilter(default_state))
async def start_logout(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_dict = await user_service.get_current_user(user_data.setdefault("access_token", "default"))

    if user_dict:
        await message.answer(
            text=USER_LEXICON_COMMANDS[message.text]["confirm"],
            reply_markup=yes_no_keyboard("logout")
        )
    else:
        await message.answer(text=USER_LEXICON_COMMANDS[message.text]["already_logout"])


@router.callback_query(F.data == "yes_logout")
async def confirm_logout(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(text=USER_LEXICON["success_logout"])


@router.callback_query(F.data == "no_logout")
async def cancel_logout(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(F.data == "exit")
async def close_keyboard(callback: CallbackQuery, state: FSMContext):
    await state.set_state(default_state)
    await callback.message.delete()

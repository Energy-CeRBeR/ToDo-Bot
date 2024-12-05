from aiogram import Router
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from .states import AuthorizeState
from .lexicon import LEXICON_COMMANDS as USER_LEXICON_COMMANDS, LEXICON as USER_LEXICON
from .services import UserService

router = Router()
user_service = UserService()


@router.message(CommandStart(), StateFilter(default_state))
async def start_bot(message: Message):
    user = await user_service.get_tg_user_by_id(message.from_user.id)
    if not user:
        await user_service.create_tg_user(
            message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name
        )

    await message.answer(USER_LEXICON_COMMANDS[message.text], parse_mode="Markdown")


@router.message(Command(commands="help"), StateFilter(default_state))
async def help_info(message: Message):
    await message.answer(text=USER_LEXICON_COMMANDS[message.text])


@router.message(Command(commands="auth"), StateFilter(default_state))
async def auth(message: Message, state: FSMContext):
    user = await user_service.get_tg_user_by_id(message.from_user.id)
    if not user:
        await user_service.create_tg_user(
            message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name
        )

    user_data = await user_service.get_current_user(user.access_token)
    if user_data:
        await message.answer(text=USER_LEXICON_COMMANDS[message.text]["already_authorized"])
    else:
        await message.answer(text=USER_LEXICON_COMMANDS[message.text]["not_authorized"])
        await state.set_state(AuthorizeState.get_email)


@router.message(StateFilter(AuthorizeState.get_email))
async def get_email(message: Message, state: FSMContext):
    email = message.text.strip()
    await state.update_data(
        email=email
    )
    await message.answer(text=USER_LEXICON["get_password"])
    await state.set_state(AuthorizeState.get_password)


@router.message(StateFilter(AuthorizeState.get_password))
async def get_password(message: Message, state: FSMContext):
    data = await state.get_data()
    email = data["email"]
    password = message.text.strip()
    await state.clear()

    user = await user_service.login_user(message.from_user.id, email, password)
    if user:
        await message.answer(text=USER_LEXICON["success_auth"])
    else:
        await message.answer(text=USER_LEXICON["invalid_auth"])

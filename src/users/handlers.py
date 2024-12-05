from aiogram import Router
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from .states import AuthorizeState
from .lexicon import LEXICON_COMMANDS as USER_LEXICON_COMMANDS, LEXICON as USER_LEXICON
from .services import UserService
from .keyboards import profile_keyboard

router = Router()
user_service = UserService()


@router.message(CommandStart(), StateFilter(default_state))
async def start_bot(message: Message):
    await message.answer(USER_LEXICON_COMMANDS[message.text], parse_mode="Markdown")


@router.message(Command(commands="help"), StateFilter(default_state))
async def help_info(message: Message):
    await message.answer(text=USER_LEXICON_COMMANDS[message.text])


@router.message(Command(commands="auth"), StateFilter(default_state))
async def auth(message: Message, state: FSMContext):
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
    await state.update_data(
        email=email
    )
    await message.answer(text=USER_LEXICON["get_password"])
    await state.set_state(AuthorizeState.get_password)


@router.message(StateFilter(AuthorizeState.get_password))
async def get_password(message: Message, state: FSMContext):
    await state.set_state(default_state)
    data = await state.get_data()
    email = data["email"]
    password = message.text.strip()

    tokens = await user_service.login_user(email, password)
    if tokens:
        await state.update_data(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"]
        )
        await message.answer(text=USER_LEXICON["success_auth"], reply_markup=profile_keyboard())
    else:
        await message.answer(text=USER_LEXICON["invalid_auth"])


@router.message(Command(commands="profile"), StateFilter(default_state))
async def auth(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_dict = await user_service.get_current_user(user_data.setdefault("access_token", "default"))

    if user_dict:
        await message.answer(text=USER_LEXICON["success_auth"], reply_markup=profile_keyboard())
        await message.answer(text=USER_LEXICON_COMMANDS[message.text]["already_authorized"])
    else:
        # Вывод сообщения о том, что пользователь не авторизирован. Либо можно создать миддлвари с проверкой на авторизацию
        pass

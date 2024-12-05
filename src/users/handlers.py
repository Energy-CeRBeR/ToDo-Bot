from aiogram import Router
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.state import default_state
from aiogram.types import Message

from .lexicon import LEXICON_COMMANDS as USER_LEXICON_COMMANDS
from .services import UserService

router = Router()
user_service = UserService()


@router.message(CommandStart(), StateFilter(default_state))
async def start_bot(message: Message):
    user = await user_service.get_tg_user_by_id(message.from_user.id)
    if not user:
        user = await user_service.create_tg_user(
            message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name
        )

    await message.answer(USER_LEXICON_COMMANDS[message.text], parse_mode="Markdown")


@router.message(Command(commands="help"), StateFilter(default_state))
async def help_info(message: Message):
    await message.answer(text=USER_LEXICON_COMMANDS[message.text])

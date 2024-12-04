from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

from src.users.lexicon import LEXICON_COMMANDS as USER_LEXICON_COMMANDS
from src.database.repositories import UserRepository

repository = UserRepository()
router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def start_bot(message: Message):
    user = await UserRepository().get_user_by_id(message.from_user.id)
    if not user:
        user = await UserRepository().create_user(
            message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name
        )

    await message.answer(USER_LEXICON_COMMANDS[message.text])



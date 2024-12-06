from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from .lexicon import LEXICON_COMMANDS as USER_LEXICON_COMMANDS, LEXICON as USER_LEXICON
from .services import CategoryService

router = Router()
category_service = CategoryService()
